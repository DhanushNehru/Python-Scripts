import pandas as pd
import argparse


def parse_vcf(vcf_file):
    contacts = []

    with open(vcf_file, "r", encoding="utf-8") as file:
        contact = {}

        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split(":", 1)
            if len(parts) != 2:
                continue

            field, value = parts
            field_name = field.split(";")[0]  # remove metadata like TEL;TYPE=CELL

            match field_name:
                case "BEGIN":
                    contact = {}

                case "FN":
                    contact["Full Name"] = value

                case "TEL":
                    contact.setdefault("Phone Numbers", []).append(value)

                case "EMAIL":
                    contact.setdefault("Emails", []).append(value)

                case "ORG":
                    contact["Organization"] = value

                case "ADR":
                    contact["Address"] = value.replace(";", " ")

                case "END":
                    contact["Phone Numbers"] = ", ".join(
                        contact.get("Phone Numbers", [])
                    )
                    contact["Emails"] = ", ".join(
                        contact.get("Emails", [])
                    )
                    contacts.append(contact)

                case _:
                    pass

    return contacts



def main():
    parser = argparse.ArgumentParser(description="Convert VCF to Excel")
    parser.add_argument("input", help="Input VCF file")
    parser.add_argument("-o", "--output", help="Output Excel file")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output if args.output else input_file.replace(".vcf", ".xlsx")

    contacts = parse_vcf(input_file)
    df = pd.DataFrame(contacts)
    df.to_excel(output_file, index=False)

    print(f"Conversion complete! Saved as {output_file}")


if __name__ == "__main__":
    main()


