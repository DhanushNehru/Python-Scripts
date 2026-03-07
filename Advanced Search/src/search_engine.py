"""
Search engine module for grep-style searching
"""
import os
import re
from typing import List, Dict, Any
from dataclasses import dataclass

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

try:
    from mutagen import File as MutagenFile
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

try:
    import xml.etree.ElementTree as ET
    XML_AVAILABLE = True
except ImportError:
    XML_AVAILABLE = False

try:
    import zipfile
    ZIPFILE_AVAILABLE = True
except ImportError:
    ZIPFILE_AVAILABLE = False

try:
    import csv
    CSV_AVAILABLE = True
except ImportError:
    CSV_AVAILABLE = False

try:
    import json as json_lib
    JSON_AVAILABLE = True
except ImportError:
    JSON_AVAILABLE = False

try:
    import sqlite3
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False


@dataclass
class SearchMatch:
    """Represents a search match in a file"""
    file_path: str
    line_number: int
    line_content: str
    match_start: int
    match_end: int
    context_before: List[str]
    context_after: List[str]


class SearchEngine:
    """Grep-style search engine"""
    
    # Class constants for supported file types
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.gif', '.bmp', '.webp'}
    FILE_METADATA_EXTENSIONS = {
        # Office & Documents
        '.pdf', '.docx', '.xlsx', '.pptx',
        # OpenDocument formats
        '.odt', '.ods', '.odp',
        # Screenwriting formats
        '.fdx', '.fountain', '.celtx',
        # Archive formats
        '.zip', '.epub',
        # Structured data
        '.csv', '.json', '.xml',
        # Database
        '.db', '.sqlite', '.sqlite3',
        # RTF
        '.rtf',
        # Audio/Video
        '.mp3', '.flac', '.m4a', '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.ogg', '.wma'
    }
    
    ARCHIVE_EXTENSIONS = {'.zip', '.epub'}
    
    def __init__(self):
        self.case_sensitive = False
        self.use_regex = False
        self.whole_word = False
        self.search_metadata = False  # Image metadata
        self.search_file_metadata = False  # File metadata (PDF, Office, audio, video)
        self.search_in_archives = False  # Search inside archive files
        self.hex_search = False  # Binary/hex search mode
        self.context_lines = 2
        self.file_extensions = []  # Empty means all files
        self.max_results = 0  # 0 = unlimited
        self.max_search_file_size = 50 * 1024 * 1024  # 50MB default
        self.network_timeout = 5  # seconds for network operations
        self._network_path_cache = {}  # Cache for network path accessibility
        self.exclude_patterns = [
            r'\.git', r'\.svn', r'__pycache__', r'node_modules',
            r'\.pyc$', r'\.exe$', r'\.dll$', r'\.so$', r'\.bin$'
        ]
    
    def search(self, root_path: str, pattern: str) -> List[SearchMatch]:
        """
        Search for pattern in files under root_path or in a specific file
        
        Args:
            root_path: Directory to search in or specific file path
            pattern: Search pattern (text or regex)
            
        Returns:
            List of SearchMatch objects
        """
        matches = []
        
        if not pattern:
            return matches
        
        # Check network path accessibility
        if self._is_network_path(root_path):
            if not self._check_network_path_accessible(root_path):
                print(f"Network path not accessible or timed out: {root_path}")
                return matches
        
        # Compile regex pattern
        try:
            if self.use_regex:
                flags = 0 if self.case_sensitive else re.IGNORECASE
                regex = re.compile(pattern, flags)
            else:
                # Escape special regex characters for literal search
                escaped_pattern = re.escape(pattern)
                if self.whole_word:
                    escaped_pattern = r'\b' + escaped_pattern + r'\b'
                flags = 0 if self.case_sensitive else re.IGNORECASE
                regex = re.compile(escaped_pattern, flags)
        except re.error as e:
            print(f"Invalid regex pattern: {e}")
            return matches
        
        # Check if root_path is a file or directory
        if os.path.isfile(root_path):
            # Search in single file
            if not self._is_excluded(root_path):
                # Check file extension filter
                if not self.file_extensions or any(root_path.endswith(ext) for ext in self.file_extensions):
                    file_matches = self._search_file(root_path, regex)
                    matches.extend(file_matches)
        else:
            # Walk directory tree
            for root, dirs, files in os.walk(root_path):
                # Early exit if max results reached (when limit is set)
                if self.max_results > 0 and len(matches) >= self.max_results:
                    break
                    
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not self._is_excluded(os.path.join(root, d))]
                
                for file in files:
                    # Early exit if max results reached (when limit is set)
                    if self.max_results > 0 and len(matches) >= self.max_results:
                        break
                        
                    file_path = os.path.join(root, file)
                    
                    # Skip excluded files
                    if self._is_excluded(file_path):
                        continue
                    
                    # Check file extension filter
                    if self.file_extensions:
                        if not any(file.endswith(ext) for ext in self.file_extensions):
                            continue
                    
                    # Search in file
                    file_matches = self._search_file(file_path, regex)
                    matches.extend(file_matches)
        
        return matches
    
    def _is_excluded(self, path: str) -> bool:
        """Check if path should be excluded"""
        path = path.replace('\\', '/')
        for pattern in self.exclude_patterns:
            if re.search(pattern, path):
                return True
        return False
    
    def _search_file(self, file_path: str, regex: re.Pattern) -> List[SearchMatch]:
        """Search for pattern in a single file (optimized)"""
        matches = []
        
        try:
            # Check file size first (skip very large files)
            file_size = os.path.getsize(file_path)
            if file_size > self.max_search_file_size:
                return matches
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Check if this is an archive file and archive search is enabled
            if self.search_in_archives and file_ext in self.ARCHIVE_EXTENSIONS:
                archive_matches = self._search_archive(file_path, regex)
                matches.extend(archive_matches)
                return matches
            
            # Check if this is an image file and image metadata search is enabled
            if self.search_metadata and file_ext in self.IMAGE_EXTENSIONS:
                # Search ONLY image metadata when metadata search is enabled
                metadata_matches = self._search_image_metadata(file_path, regex)
                matches.extend(metadata_matches)
                return matches  # Skip text search for images
            
            # Check if this is a file with metadata and file metadata search is enabled
            if self.search_file_metadata and file_ext in self.FILE_METADATA_EXTENSIONS:
                # Search ONLY file metadata when file metadata search is enabled
                metadata_matches = self._search_file_metadata(file_path, regex)
                matches.extend(metadata_matches)
                return matches  # Skip text search for these files
            
            # If either metadata search is enabled but this file doesn't match, skip it
            if self.search_metadata or self.search_file_metadata:
                return matches
            
            # Binary/hex search mode
            if self.hex_search:
                hex_matches = self._search_binary(file_path, regex)
                matches.extend(hex_matches)
                return matches
            
            # Try to read as text file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Search each line
            for i, line in enumerate(lines):
                for match in regex.finditer(line):
                    # Get context lines
                    context_before = []
                    context_after = []
                    
                    start_idx = max(0, i - self.context_lines)
                    end_idx = min(len(lines), i + self.context_lines + 1)
                    
                    if self.context_lines > 0:
                        context_before = [lines[j].rstrip('\n\r') for j in range(start_idx, i)]
                        context_after = [lines[j].rstrip('\n\r') for j in range(i + 1, end_idx)]
                    
                    search_match = SearchMatch(
                        file_path=file_path,
                        line_number=i + 1,  # 1-based line numbers
                        line_content=line.rstrip('\n\r'),
                        match_start=match.start(),
                        match_end=match.end(),
                        context_before=context_before,
                        context_after=context_after
                    )
                    matches.append(search_match)
        
        except (IOError, OSError, UnicodeDecodeError):
            # Skip files that can't be read
            pass
        
        return matches
    
    def _search_image_metadata(self, file_path: str, regex: re.Pattern) -> List[SearchMatch]:
        """Search image metadata for pattern matches"""
        matches = []
        
        if not PILLOW_AVAILABLE:
            return matches
        
        try:
            with Image.open(file_path) as img:
                metadata = self._extract_image_metadata(img)
                
                # Convert metadata to searchable text
                line_num = 1
                for key, value in metadata.items():
                    # Create searchable line from metadata
                    line_text = f"{key}: {value}"
                    
                    # Search for matches in this metadata line
                    for match in regex.finditer(line_text):
                        search_match = SearchMatch(
                            file_path=file_path,
                            line_number=line_num,
                            line_content=line_text,
                            match_start=match.start(),
                            match_end=match.end(),
                            context_before=[],
                            context_after=[]
                        )
                        matches.append(search_match)
                    
                    line_num += 1
        
        except Exception:
            # Skip files that can't be opened as images
            pass
        
        return matches
    
    def _extract_image_metadata(self, img: 'Image.Image') -> Dict[str, Any]:
        """Extract metadata from an image"""
        metadata = {}
        
        # Basic image info
        metadata['Format'] = img.format or 'Unknown'
        metadata['Mode'] = img.mode
        metadata['Size'] = f"{img.width}x{img.height}"
        
        # EXIF data
        try:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, f"Unknown_{tag_id}")
                    
                    # Handle GPS data specially
                    if tag_name == "GPSInfo":
                        gps_data = {}
                        for gps_tag_id, gps_value in value.items():
                            gps_tag_name = GPSTAGS.get(gps_tag_id, f"GPS_{gps_tag_id}")
                            gps_data[gps_tag_name] = str(gps_value)
                        metadata[tag_name] = str(gps_data)
                    else:
                        # Convert value to string, handle bytes
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8', errors='ignore')
                            except Exception:
                                value = str(value)
                        metadata[tag_name] = str(value)
        except (AttributeError, KeyError, TypeError):
            pass
        
        # PNG info
        if hasattr(img, 'info'):
            for key, value in img.info.items():
                if key not in metadata:
                    metadata[f"PNG_{key}"] = str(value)
        
        return metadata
    
    def _search_file_metadata(self, file_path: str, regex: re.Pattern) -> List[SearchMatch]:
        """Search file metadata for pattern matches"""
        matches = []
        metadata = self._extract_file_metadata(file_path)
        
        # Convert metadata to searchable text
        line_num = 1
        for key, value in metadata.items():
            # Create searchable line from metadata
            line_text = f"{key}: {value}"
            
            # Search for matches in this metadata line
            for match in regex.finditer(line_text):
                search_match = SearchMatch(
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line_text,
                    match_start=match.start(),
                    match_end=match.end(),
                    context_before=[],
                    context_after=[]
                )
                matches.append(search_match)
            
            line_num += 1
        
        return matches
    
    def _extract_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from various file types"""
        metadata = {}
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            # Screenwriting formats
            if file_ext == '.fdx' and XML_AVAILABLE:
                # Final Draft XML format
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                # Extract metadata from FinalDraft namespace
                for content in root.findall('.//{http://www.finaldraft.com/FDX}Content'):
                    content_type = content.get('Type', '')
                    if content_type:
                        metadata[f'FDX_{content_type}'] = content.text[:200] if content.text else ''
                
                # Count pages, scenes, etc
                scenes = root.findall('.//{http://www.finaldraft.com/FDX}Paragraph[@Type="Scene Heading"]')
                metadata['Scenes'] = str(len(scenes))
                
            elif file_ext == '.fountain':
                # Fountain format (plain text with special syntax)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                # Extract title page metadata (key: value format at start)
                in_title_page = True
                scene_count = 0
                
                for line in lines:
                    if in_title_page and ':' in line and not line.startswith('.'):
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()[:200]
                    elif line.strip() == '':
                        in_title_page = False
                    elif line.strip().startswith(('INT.', 'EXT.', 'INT/EXT', 'I/E')):
                        scene_count += 1
                
                metadata['Scenes'] = str(scene_count)
                
            elif file_ext == '.celtx' and ZIPFILE_AVAILABLE:
                # Celtx is a ZIP archive with HTML/XML
                with zipfile.ZipFile(file_path, 'r') as z:
                    if 'project.celtx' in z.namelist():
                        content = z.read('project.celtx').decode('utf-8', errors='ignore')
                        # Basic metadata extraction
                        metadata['Type'] = 'Celtx Project'
                        metadata['Files'] = str(len(z.namelist()))
            
            # Archive formats
            elif file_ext == '.zip' and ZIPFILE_AVAILABLE:
                with zipfile.ZipFile(file_path, 'r') as z:
                    metadata['Files'] = str(len(z.namelist()))
                    metadata['Compressed Size'] = f"{os.path.getsize(file_path) / 1024:.1f} KB"
                    # List first 10 files
                    file_list = z.namelist()[:10]
                    metadata['Contents'] = ', '.join(file_list)
                    if len(z.namelist()) > 10:
                        metadata['Contents'] += f' ... and {len(z.namelist()) - 10} more'
                        
            elif file_ext == '.epub' and ZIPFILE_AVAILABLE:
                # EPUB is a ZIP with specific structure
                with zipfile.ZipFile(file_path, 'r') as z:
                    # Try to read metadata from content.opf
                    for name in z.namelist():
                        if name.endswith('.opf'):
                            content = z.read(name).decode('utf-8', errors='ignore')
                            if XML_AVAILABLE:
                                try:
                                    root = ET.fromstring(content)
                                    # Extract Dublin Core metadata
                                    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
                                    for elem in root.findall('.//dc:title', ns):
                                        metadata['Title'] = elem.text[:200] if elem.text else ''
                                    for elem in root.findall('.//dc:creator', ns):
                                        metadata['Author'] = elem.text[:200] if elem.text else ''
                                    for elem in root.findall('.//dc:publisher', ns):
                                        metadata['Publisher'] = elem.text[:200] if elem.text else ''
                                    for elem in root.findall('.//dc:language', ns):
                                        metadata['Language'] = elem.text if elem.text else ''
                                except Exception:
                                    pass
                            break
            
            # Structured data formats
            elif file_ext == '.csv' and CSV_AVAILABLE:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)
                    if headers:
                        metadata['Columns'] = ', '.join(headers[:10])
                        if len(headers) > 10:
                            metadata['Columns'] += f' ... ({len(headers)} total)'
                    
                    # Count rows (limit to avoid performance issues)
                    row_count = sum(1 for _ in reader)
                    metadata['Rows'] = str(row_count + 1)  # +1 for header
                    
            elif file_ext == '.json' and JSON_AVAILABLE:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        data = json_lib.load(f)
                        metadata['Type'] = type(data).__name__
                        if isinstance(data, dict):
                            metadata['Keys'] = ', '.join(list(data.keys())[:10])
                            if len(data) > 10:
                                metadata['Keys'] += f' ... ({len(data)} total)'
                        elif isinstance(data, list):
                            metadata['Items'] = str(len(data))
                    except Exception:
                        metadata['Type'] = 'Invalid JSON'
                        
            elif file_ext == '.xml' and XML_AVAILABLE:
                tree = ET.parse(file_path)
                root = tree.getroot()
                metadata['Root Tag'] = root.tag
                metadata['Namespace'] = root.tag.split('}')[0][1:] if '}' in root.tag else 'None'
                metadata['Child Elements'] = str(len(list(root)))
                
                # Extract common attributes
                for key, value in root.attrib.items():
                    metadata[f'Attr_{key}'] = str(value)[:200]
            
            # OpenDocument formats
            elif file_ext in {'.odt', '.ods', '.odp'} and ZIPFILE_AVAILABLE:
                with zipfile.ZipFile(file_path, 'r') as z:
                    if 'meta.xml' in z.namelist():
                        content = z.read('meta.xml').decode('utf-8', errors='ignore')
                        if XML_AVAILABLE:
                            try:
                                root = ET.fromstring(content)
                                ns = {
                                    'meta': 'urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
                                    'dc': 'http://purl.org/dc/elements/1.1/'
                                }
                                for elem in root.findall('.//dc:title', ns):
                                    metadata['Title'] = elem.text[:200] if elem.text else ''
                                for elem in root.findall('.//dc:creator', ns):
                                    metadata['Creator'] = elem.text[:200] if elem.text else ''
                                for elem in root.findall('.//dc:subject', ns):
                                    metadata['Subject'] = elem.text[:200] if elem.text else ''
                                for elem in root.findall('.//meta:keyword', ns):
                                    metadata['Keywords'] = elem.text[:200] if elem.text else ''
                            except Exception:
                                pass
            
            # PDF files
            elif file_ext == '.pdf' and PYPDF2_AVAILABLE:
                with open(file_path, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    if pdf.metadata:
                        for key, value in pdf.metadata.items():
                            metadata[f"PDF_{key.strip('/')}"] = str(value)[:200]
                    metadata['PDF_Pages'] = str(len(pdf.pages))
            
            # Word documents
            elif file_ext == '.docx' and DOCX_AVAILABLE:
                doc = docx.Document(file_path)
                props = doc.core_properties
                if props.author: metadata['Author'] = props.author
                if props.title: metadata['Title'] = props.title
                if props.subject: metadata['Subject'] = props.subject
                if props.keywords: metadata['Keywords'] = props.keywords
                if props.category: metadata['Category'] = props.category
                if props.comments: metadata['Comments'] = props.comments[:200]
                if props.created: metadata['Created'] = str(props.created)
                if props.modified: metadata['Modified'] = str(props.modified)
                metadata['Paragraphs'] = str(len(doc.paragraphs))
            
            # Excel files
            elif file_ext == '.xlsx' and OPENPYXL_AVAILABLE:
                wb = openpyxl.load_workbook(file_path, read_only=True)
                props = wb.properties
                if props.creator: metadata['Creator'] = props.creator
                if props.title: metadata['Title'] = props.title
                if props.subject: metadata['Subject'] = props.subject
                if props.keywords: metadata['Keywords'] = props.keywords
                if props.category: metadata['Category'] = props.category
                if props.description: metadata['Description'] = props.description[:200]
                if props.created: metadata['Created'] = str(props.created)
                if props.modified: metadata['Modified'] = str(props.modified)
                metadata['Sheets'] = str(len(wb.sheetnames))
                wb.close()
            
            # Audio/Video files
            elif file_ext in {'.mp3', '.flac', '.m4a', '.ogg', '.wma', '.mp4', '.avi', '.mkv', '.mov', '.wmv'} and MUTAGEN_AVAILABLE:
                audio = MutagenFile(file_path)
                if audio and audio.tags:
                    for key, value in audio.tags.items():
                        # Clean up tag name
                        clean_key = str(key).replace('\x00', '')
                        metadata[f"Audio_{clean_key}"] = str(value)[:200]
                if audio and hasattr(audio.info, 'length'):
                    metadata['Duration'] = f"{int(audio.info.length // 60)}:{int(audio.info.length % 60):02d}"
                if audio and hasattr(audio.info, 'bitrate'):
                    metadata['Bitrate'] = f"{audio.info.bitrate // 1000} kbps"
            
            # SQLite databases
            elif file_ext in {'.db', '.sqlite', '.sqlite3'} and SQLITE_AVAILABLE:
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                
                # Get all table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
                tables = [row[0] for row in cursor.fetchall()]
                metadata['Tables'] = ', '.join(tables)
                metadata['Table Count'] = str(len(tables))
                
                # Get schema info for each table
                for table in tables[:5]:  # Limit to first 5 tables
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = [row[1] for row in cursor.fetchall()]
                    metadata[f'Table_{table}_Columns'] = ', '.join(columns)
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    row_count = cursor.fetchone()[0]
                    metadata[f'Table_{table}_Rows'] = str(row_count)
                
                conn.close()
            
            # RTF files
            elif file_ext == '.rtf':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000)  # Read first 1KB
                    
                    # Extract basic RTF metadata from header
                    # RTF format: {\info{\title ...}{\author ...}}
                    import re
                    title_match = re.search(r'\\title\s+([^}]+)', content)
                    if title_match:
                        metadata['Title'] = title_match.group(1).strip()[:200]
                    
                    author_match = re.search(r'\\author\s+([^}]+)', content)
                    if author_match:
                        metadata['Author'] = author_match.group(1).strip()[:200]
                    
                    subject_match = re.search(r'\\subject\s+([^}]+)', content)
                    if subject_match:
                        metadata['Subject'] = subject_match.group(1).strip()[:200]
                    
                    # Get RTF version
                    version_match = re.search(r'\\rtf(\d+)', content)
                    if version_match:
                        metadata['RTF Version'] = version_match.group(1)
        
        except Exception as e:
            # If metadata extraction fails, just skip this file
            pass
        
        return metadata
    
    def _search_archive(self, file_path: str, regex: re.Pattern) -> List[SearchMatch]:
        """Search inside archive files (ZIP, EPUB, etc.)"""
        matches = []
        
        if not ZIPFILE_AVAILABLE:
            return matches
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                for member in zf.namelist():
                    # Skip directories
                    if member.endswith('/'):
                        continue
                    
                    # Check file size
                    member_info = zf.getinfo(member)
                    if member_info.file_size > self.max_search_file_size:
                        continue
                    
                    try:
                        # Read file content from archive
                        content = zf.read(member)
                        
                        # Try to decode as text
                        try:
                            text = content.decode('utf-8', errors='ignore')
                            lines = text.split('\n')
                            
                            # Search each line
                            for i, line in enumerate(lines):
                                for match in regex.finditer(line):
                                    # Get context lines
                                    context_before = []
                                    context_after = []
                                    
                                    start_idx = max(0, i - self.context_lines)
                                    end_idx = min(len(lines), i + self.context_lines + 1)
                                    
                                    if self.context_lines > 0:
                                        context_before = [lines[j].rstrip('\n\r') for j in range(start_idx, i)]
                                        context_after = [lines[j].rstrip('\n\r') for j in range(i + 1, end_idx)]
                                    
                                    # Use archive_path/internal_path format
                                    search_match = SearchMatch(
                                        file_path=f"{file_path}/{member}",
                                        line_number=i + 1,
                                        line_content=line.rstrip('\n\r'),
                                        match_start=match.start(),
                                        match_end=match.end(),
                                        context_before=context_before,
                                        context_after=context_after
                                    )
                                    matches.append(search_match)
                        except UnicodeDecodeError:
                            # Binary file inside archive, skip
                            pass
                    except Exception:
                        # Skip files that can't be read from archive
                        pass
        except Exception:
            # Skip archives that can't be opened
            pass
        
        return matches
    
    def _search_binary(self, file_path: str, regex: re.Pattern) -> List[SearchMatch]:
        """Search binary files for hex patterns"""
        matches = []
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Convert pattern to bytes if it looks like hex
            pattern_str = regex.pattern
            
            # Try to match as both text and hex
            # Search for text pattern in binary content
            try:
                text_content = content.decode('utf-8', errors='ignore')
                for match in regex.finditer(text_content):
                    # Calculate byte offset
                    byte_offset = match.start()
                    
                    # Get hex dump context (16 bytes before and after)
                    start = max(0, byte_offset - 16)
                    end = min(len(content), byte_offset + 16)
                    hex_context = content[start:end].hex(' ')
                    
                    search_match = SearchMatch(
                        file_path=file_path,
                        line_number=byte_offset,  # Using offset as "line"
                        line_content=f"Offset {byte_offset:08x}: {hex_context}",
                        match_start=match.start(),
                        match_end=match.end(),
                        context_before=[],
                        context_after=[]
                    )
                    matches.append(search_match)
            except Exception:
                pass
            
        except Exception:
            pass
        
        return matches
    
    def _is_network_path(self, path: str) -> bool:
        """Check if path is a network/UNC path"""
        # UNC paths start with \\
        return path.startswith('\\\\') or path.startswith('//')
    
    def _check_network_path_accessible(self, path: str) -> bool:
        """Check if network path is accessible with timeout"""
        # Check cache first
        if path in self._network_path_cache:
            return self._network_path_cache[path]
        
        try:
            # Try to check if path exists with timeout
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(os.path.exists, path)
                accessible = future.result(timeout=self.network_timeout)
                self._network_path_cache[path] = accessible
                return accessible
        except Exception:
            # If timeout or error, assume not accessible
            self._network_path_cache[path] = False
            return False
    
    def set_case_sensitive(self, enabled: bool):
        """Enable or disable case-sensitive search"""
        self.case_sensitive = enabled
    
    def set_regex(self, enabled: bool):
        """Enable or disable regex search"""
        self.use_regex = enabled
    
    def set_whole_word(self, enabled: bool):
        """Enable or disable whole word search"""
        self.whole_word = enabled
    
    def set_search_metadata(self, enabled: bool):
        """Enable or disable metadata search for images"""
        self.search_metadata = enabled
    
    def set_search_file_metadata(self, enabled: bool):
        """Enable or disable metadata search for files (PDF, Office, audio, video)"""
        self.search_file_metadata = enabled
    
    def set_search_in_archives(self, enabled: bool):
        """Enable or disable searching inside archive files"""
        self.search_in_archives = enabled
    
    def set_hex_search(self, enabled: bool):
        """Enable or disable binary/hex search mode"""
        self.hex_search = enabled
    
    def clear_network_cache(self):
        """Clear the network path accessibility cache"""
        self._network_path_cache.clear()
    
    def set_context_lines(self, lines: int):
        """Set number of context lines to include"""
        self.context_lines = max(0, lines)
    
    def set_file_extensions(self, extensions: List[str]):
        """Set file extensions to filter (e.g., ['.py', '.txt'])"""
        self.file_extensions = extensions
    
    def add_exclude_pattern(self, pattern: str):
        """Add a pattern to exclude from search"""
        self.exclude_patterns.append(pattern)
