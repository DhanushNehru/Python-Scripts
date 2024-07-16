<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spotify-Youtube-Music-Exchange</title>
</head>

<body>

  <h1>Spotify-Youtube-Music-Exchange</h1>

  <p>This Python script allows you to exchange songs and playlists between Spotify and YouTube Music.</p>

  <h2>Requirements</h2>

  <p>Make sure you have the following libraries installed:</p>

  <ul>
    <li><a href="https://pypi.org/project/fuzzywuzzy/" target="_blank">fuzzywuzzy==0.18.0</a></li>
    <li><a href="https://pandas.pydata.org/" target="_blank">pandas==1.3.2</a></li>
    <li><a href="https://docs.python-requests.org/en/master/" target="_blank">requests==2.31.0</a></li>
    <li><a href="https://spotipy.readthedocs.io/en/2.23.0/" target="_blank">spotipy==2.23.0</a></li>
    <li><a href="https://ytmusicapi.readthedocs.io/en/stable/" target="_blank">ytmusicapi==1.3.2</a></li>
  </ul>

  <p>You can install these libraries using the following command:</p>

  <pre><code>pip install fuzzywuzzy==0.18.0 pandas==1.3.2 requests==2.31.0 spotipy==2.23.0 ytmusicapi==1.3.2</code></pre>

  <h2>Setup "header_auth.json" (Browser Authentication) on local system:</h2>

  <ol>
    <li>Follow the <a href="https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html" target="_blank">documentation link</a> to set up "header_auth.json" for Browser Authentication.</li>
    <li>Save the generated "header_auth.json" file in the root directory of this project.</li>
  </ol>

  <h2>Usage</h2>

  <ol>
    <li>Clone the repository:</li>
  </ol>

  <pre><code>git clone https://github.com/yourusername/Spotify-Youtube-Music-Exchange.git
cd Spotify-Youtube-Music-Exchange</code></pre>

  <ol start="2">
    <li>Install the required libraries:</li>
  </ol>

  <pre><code>pip install -r requirements.txt</code></pre>

  <ol start="3">
    <li>Run the script:</li>
  </ol>

  <pre><code>python playlistexchange.py</code></pre>

  <p>Follow the on-screen instructions to exchange songs and playlists between Spotify and YouTube Music.</p>

  <h2>Contributing</h2>

  <p>If you'd like to contribute to this project, please fork the repository and submit a pull request. Issues and feature requests are welcome!</p>

  <h2>License</h2>

  <p>This project is licensed under the MIT License - see the <a href="LICENSE" target="_blank">LICENSE</a> file for details.</p>

</body>

</html>

<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->