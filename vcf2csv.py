import argparse
import csv
import os
import vobject

def fix_vcf(vcf_filename, fixed_vcf_filename):
    """
    This function reads a vCard file and writes a new vCard file with any lines that end with '='
    concatenated with the next line. This is necessary because some vCard files split long lines
    into multiple lines by ending each line with '='.
    :param vcf_filename: The name of the input vCard file.
    :param fixed_vcf_filename: The name of the output vCard file.
    """
    with open(vcf_filename, 'r') as source_file, open(fixed_vcf_filename, 'w') as target_file:
        previous_line = ''
        for line in source_file:
            if previous_line.endswith('=\n') and not line.startswith(' '):
                target_file.write(' ' + line)
            else:
                target_file.write(line)
            previous_line = line


def vcf_to_csv(vcf_filename, csv_filename):
    """
    This function reads a vCard file and writes a CSV file containing the contact information
    from the vCard file. The CSV file will have columns for the contact's name, email address,
    phone number, and any other fields that are present in the vCard file.
    :param vcf_filename: The name of the input vCard file.
    :param csv_filename: The name of the output CSV file.
    """
    # Encoding is changed for Turkish characters, change for your set
    with open(vcf_filename, 'r', encoding='ISO-8859-9') as source_file:
        vcard_data = vobject.readComponents(source_file.read())
        contact_list = []

        for vcard in vcard_data:
            contact = {}
            for field in vcard.contents:
                if field == "photo":  # Skip photos
                    continue
                if field in ['n', 'fn', 'email', 'tel']:
                    if isinstance(vcard.contents[field][0].value, str):
                        contact[field] = vcard.contents[field][0].value
                    else:
                        contact[field] = " ".join(vcard.contents[field][0].value.__dict__.values())
            contact_list.append(contact)

        keys = contact_list[0].keys()

        with open(csv_filename, 'w', newline='', encoding="ISO-8859-9") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(contact_list)

def main():
    parser = argparse.ArgumentParser(description="Convert vCard (.vcf) files to CSV")
    parser.add_argument("input_vcf", help="Path to the input vCard file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("--fixed", dest="fixed_vcf", help="Optional path for the intermediate fixed vCard file")
    args = parser.parse_args()

    fixed_path = args.fixed_vcf or os.path.splitext(args.input_vcf)[0] + "_fixed.vcf"

    fix_vcf(args.input_vcf, fixed_path)
    vcf_to_csv(fixed_path, args.output_csv)


if __name__ == "__main__":
    main()
