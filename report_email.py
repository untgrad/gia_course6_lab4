#!/usr/bin/env python3
import os
import datetime
import reports
import emails


# read text entry:
def getDesc(file):
    with open(file) as f:
        lines = f.read().strip().splitlines()
    name_field = "name: {}".format(lines[0])
    weight_field = "weight: {}".format(lines[1])
    return "{}<br/>{}<br/><br/>".format(name_field, weight_field)


def main():
    # set text dir & gather files:
    txt_dir = "supplier-data/descriptions/"
    txt_files = [txt_dir + f for f in os.listdir(txt_dir) if f.endswith(".txt")]

    # set report file:
    report_file = "/tmp/processed.pdf"

    # generate report body:
    report_body = ""
    for file in txt_files:
        report_body += getDesc(file)

    # set report title:
    today = datetime.datetime.today()
    report_title = "Processed Update on {} {}, {}".format(
        today.strftime("%B"), today.day, today.year
    )

    # generate report file:
    reports.generate_report(report_file, report_title, report_body)

    # generate & send email report:
    content = {
        "sender": "automation@example.com",
        "receiver": "{}@example.com".format(os.environ.get("USER")),
        "subject": "Upload Completed - Online Fruit Store",
        "body": "All fruits are uploaded to our website successfully. A detailed list is attached to this email.",
        "attachment": report_file,
    }
    message = emails.generate_email(**content)
    emails.send_email(message)


if __name__ == "__main__":
    main()
