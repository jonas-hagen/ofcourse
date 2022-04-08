#! /usr/bin/env python3
import sys
from os import path
import click
from tabulate import tabulate
from ofcourse import dumpers
from ofcourse import parsers
from ofcourse import renderer


@click.group()
def cli():
    pass


@cli.group("people")
def people_group():
    pass


@cli.group("course")
def course_group():
    pass


@people_group.command("normalize")
@click.argument(
    "filename",
    default="./people.yml",
    type=click.Path(exists=True, dir_okay=False, writable=True),
)
def people_normalize(filename):
    with open(filename, "r") as f:
        person_list = parsers.person_list_parser(f)
    if not person_list:
        exit()
    with open(filename, "w") as f:
        dumpers.person_list_yaml_dumper(f, person_list)


@course_group.command("print")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.argument(
    "people-file", default="./people.yml", type=click.Path(exists=True, dir_okay=False)
)
def course_print(filename, people_file):
    with open(people_file, "r") as f:
        person_list = parsers.person_list_parser(f)
    with open(filename, "r") as f:
        course = parsers.course_parser(f, person_list)
    dumpers.course_text_dumper(sys.stdout, course)


@course_group.command("render")
@click.argument(
    "filename", type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
@click.argument("template-file", type=click.Path(exists=True, dir_okay=False))
@click.argument(
    "people-file",
    default="./people.yml",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.option(
    "--output",
    "-o",
    default=None,
    type=click.Path(resolve_path=True),
    help="Write to this file or path.",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Overwrite existing files, only if output is specified.",
)
@click.option(
    "--each-person/--whole-course",
    default=False,
    help="Write a file for each course / person.",
)
@click.option(
    "--env",
    "-e",
    default="default",
    help="Jinja2 enviroment to use: " + ", ".join(renderer.environments.keys()),
    type=click.Choice(list(renderer.environments.keys())),
)
def course_render(
    filename, template_file, people_file, output, force, each_person, env
):
    with open(people_file, "r") as f:
        person_list = parsers.person_list_parser(f)
    with open(filename, "r") as f:
        course = parsers.course_parser(f, person_list)

    if output is None:
        # base of coursefle, ext of template
        output = path.dirname(filename)

    if not each_person:
        if path.isdir(output):
            force = False
            dirname = output
            base = path.basename(path.splitext(filename)[0])
            ext = path.splitext(template_file)[1]
            output = path.join(dirname, base + ext)
        if path.isfile(output) and not force:
            raise FileExistsError(output)

        with open(output, "w") as f:
            f.write(renderer.render(template_file, env, c=course))
        print(output)
    else:
        if not path.isdir(output):
            raise FileNotFoundError("Directory " + output)
        else:
            dirname = output
            base = path.basename(path.splitext(filename)[0])
            ext = path.splitext(template_file)[1]

        for person in course.participants:
            output = path.join(dirname, base + "_" + person.identifier + ":2,DS")
            with open(output, "w") as f:
                f.write(renderer.render(template_file, env, p=person, c=course))
            print(output)


@course_group.command("email")
@click.argument(
    "subject",
    type=str,
)
@click.argument(
    "course-file", type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
@click.argument("template-file", type=click.Path(exists=True, dir_okay=False))
@click.argument(
    "people-file",
    default="./people.yml",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.option(
    "--test",
    "-t",
    "test_addr",
    default=None,
    help="Run a test (send to From) or send mails for real.",
)
@click.option("--send/--no-send", default=False)
@click.option(
    "--from",
    "-f",
    "from_addr",
    required=True,
    help="The From address.",
)
@click.option(
    "--attach",
    "-a",
    required=False,
    multiple=True,
    help="File(s) to attach.",
)
def course_email(
    subject, course_file, template_file, people_file, test_addr, send, from_addr, attach
):
    import os
    import smtplib
    import email.utils

    import mimetypes
    from email import encoders
    from email.mime.audio import MIMEAudio
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import email.policy

    with open(people_file, "r") as f:
        person_list = parsers.person_list_parser(f)
    with open(course_file, "r") as f:
        course = parsers.course_parser(f, person_list)

    smtp_server = os.environ["SMTP_SERVER"]
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]

    def get_attachement(filename):
        filename_base = os.path.basename(filename)
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = "application/octet-stream"
        print(f"  Attaching {filename_base} as {ctype}")
        maintype, subtype = ctype.split("/", 1)
        if maintype == "text":
            with open(filename) as fp:
                # Note: we should handle calculating the charset
                part = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == "image":
            with open(filename, "rb") as fp:
                part = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == "audio":
            with open(filename, "rb") as fp:
                part = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(filename, "rb") as fp:
                part = MIMEBase(maintype, subtype)
                part.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(part)
        # Set the filename parameter
        part.add_header("Content-Disposition", "attachment", filename=filename_base)
        return part

    messages = []
    for person in course.participants:
        msg = MIMEMultipart(policy=email.policy.strict)

        print(f"Preparing message to {person.full_name}.")

        # Outer headers
        subject_prefix = "[Test] " if test_addr else ""
        msg["Subject"] = subject_prefix + subject
        msg["From"] = from_addr
        msg["Sender"] = from_addr
        msg["Bcc"] = from_addr
        msg["Date"] = email.utils.formatdate(localtime=True)
        to_addr = test_addr or person.primary_email
        msg["To"] = f"{person.full_name} <{to_addr}>"

        # Body (the message)
        body_text = renderer.render(template_file, "default", p=person, c=course)
        body = MIMEText(body_text, "plain")
        msg.attach(body)

        # Attachements
        for filename in attach:
            filename_r = renderer.render_string(filename, "default", p=person, c=course)
            try:
                part = get_attachement(filename_r)
            except FileNotFoundError as e:
                print("  File not found, skipping attach: ", e)
            else:
                msg.attach(part)

        messages.append(msg)

    if send and input("Do You Want To Send Messages? [y/N]") == "y":
        smtp = smtplib.SMTP(smtp_server, port=587)
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)

        for msg in messages:
            print("Sending message to: ", msg["To"])
            smtp.send_message(msg)

        smtp.close()
    else:
        print("NOT sending messages")


if __name__ == "__main__":
    cli()
