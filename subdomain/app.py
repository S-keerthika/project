from flask import Flask, render_template, request
import dns.resolver
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']


def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Set up the SMTP server
    smtp_server = smtplib.SMTP('smtppro.zoho.in', 587)
    smtp_server.starttls()  # Enable TLS encryption
    smtp_server.login(sender_email, sender_password)  # Log in to the SMTP server

    # Create the email message
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    # Send the email
    smtp_server.sendmail(sender_email, recipient_email, message.as_string())

    # Close the connection to the SMTP server
    smtp_server.quit()


def fetch_email_addresses(domain):
    email_addresses = set()

    try:
        # Query MX records for the domain
        mx_records = dns.resolver.resolve(domain, 'MX')

        # Extract email addresses from MX records
        for mx_record in mx_records:
            mail_server = str(mx_record.exchange)
            email_addresses.add(mail_server)
    except dns.resolver.NoAnswer:
        print(f"No MX records found for {domain}")
    except dns.resolver.NXDOMAIN:
        print("Domain does not exist:", domain)
    except dns.exception.DNSException as e:
        print("DNS resolution error:", e)

    return email_addresses


def fetch_record_type(domain):
    record_types = ['A', 'AAAA', 'ALIAS', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT']
    results = []
    for record_type in record_types:
        try:
            answer = resolver.resolve(domain, record_type)
            for server in answer:
                results.append(f"{record_type}: {server.to_text()}")
        except dns.resolver.NoAnswer:
            results.append(f"No {record_type} records found")
        except dns.resolver.NXDOMAIN:
            results.append("Domain does not exist")
        except dns.exception.DNSException as e:
            results.append(f"DNS resolution error: {e}")
    return results


def fetch_fingerprint(domain):
    try:
        # Send an HTTP GET request to the domain
        response = requests.get(f"http://{domain}")
        # Check if the response status code is 404
        if response.status_code == 404:
            # Extract the error message from the response content
            error_message = response.text

            # Check if the error message matches any known vulnerable patterns
            vulnerable_patterns = ["The specified bucket does not exist"]
            for pattern in vulnerable_patterns:
                if pattern in error_message:
                    print(f"This subdomain {domain} contains vulnerability {pattern}.")
                    sender_email = 'keerthika@subdomain.life'
                    sender_password = 'xDZruNXgVi1u'
                    recipient_email = 'keerthika@subdomain.life'
                    subject = 'SUBDOMAIN HAS VULNERABLE'

                    body = f"This subdomain {domain} contains vulnerability {pattern}."
                    formatted_string = body.format(domain=domain, vulnerable_patterns=vulnerable_patterns)

                    # Send the email
                    send_email(sender_email, sender_password, recipient_email, subject, formatted_string)
                    print("Mail sent")
                    return
            # If the error message does not match any known vulnerable patterns,
            # return a generic error message
           
            print("Not vulnerable")

    except Exception as e:
        print("Error:", str(e))


def subdomain_records(domain):
    with open('subdomains-1000.txt', 'r') as file:
        words = file.read().splitlines()
    subdomains = [word.strip() for word in words]

    results = []

    for subdomain in subdomains:
        try:
            ip_value = dns.resolver.resolve(f'{subdomain}.{domain}', 'A')
            if ip_value:
                result = dns.resolver.resolve(f'{subdomain}.{domain}', 'CNAME')
                for cnameval in result:
                    subdomain_url = f'{subdomain}.{domain}'
                    results.append(f'Subdomain URL: {subdomain_url}, CNAME: {cnameval.target}')
                    fetch_fingerprint(subdomain_url)  # Function to fetch fingerprint
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.LifetimeTimeout:
            pass
        except dns.exception.DNSException as e:
            results.append(f"DNS resolution error: {e}")
            pass

    return results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def scan():
    if request.method == 'POST':
        domain = request.form['domain']
        record_types = fetch_record_type(domain)
        subdomain_results = subdomain_records(domain)
        email_addresses = fetch_email_addresses(domain)
        return render_template('results.html', domain=domain, record_types=record_types,
                               subdomain_results=subdomain_results, email_addresses=email_addresses)
    else:
        return 'Invalid Request'


if __name__ == "__main__":
    app.run(debug=True)
