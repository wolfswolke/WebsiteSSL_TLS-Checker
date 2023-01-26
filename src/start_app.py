import ssl
import socket
import OpenSSL
from datetime import datetime

hostname = input("Enter a website or IP address to check: ")
conn = None

try:
    sock = socket.create_connection((hostname, 80))
    print("HTTP is supported")
except socket.gaierror:
    print("Please enter a Valid URL or IP.")
    exit()
except Exception as e:
    print(type(e))
    print("HTTP is not supported")

try:
    https_sock = socket.create_connection((hostname, 443))
    context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None)
    conn = context.wrap_socket(https_sock, server_hostname=hostname)
    cert = conn.getpeercert(binary_form=True)
    print("HTTPS is supported")
except ssl.SSLCertVerificationError:
    print("HTTPS is not supported")

if conn:
    try:
        print(f"TLS version in use: {conn.version()}")
    except Exception as e:
        print(e)

    try:
        cert = ssl.DER_cert_to_PEM_cert(cert)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        if x509.get_issuer() == x509.get_subject():
            print("The certificate is self-signed")
        else:
            print("The certificate is not self-signed")
    except Exception as e:
        print(e)

    try:
        expiry_date = datetime.strptime(x509.get_notAfter().decode(), '%Y%m%d%H%M%SZ')
        if datetime.utcnow() > expiry_date:
            print("The certificate has expired")
        else:
            print("The certificate is still valid")
            print("The certificate will expire on this Date: {}".format(expiry_date))
    except Exception as e:
        print(e)
        print("Unable to check if the certificate is still valid")
else:
    cert = ssl.get_server_certificate((hostname, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    if x509.get_issuer() == x509.get_subject():
        print("The website uses a self-signed certificate.")
    else:
        print("No Certificate Info found.")

