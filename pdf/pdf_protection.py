import PyPDF2
import sys

def create_password_protection(input_pdf, output_pdf, password):
    try:
        with open(input_pdf, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            writer = PyPDF2.PdfWriter()

            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

            writer.encrypt(password)
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            
            print(f'Password-protected PDF saved as {output_pdf}')
    except FileNotFoundError:
        print(f'The file {input_pdf} was not found')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    if len(sys.argv) != 4:
        print('Usage: python pdf_protection.py <input_pdf> <output_pdf> <password>')
        sys.exit(1)
    else:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        password = sys.argv[3]
        create_password_protection(input_pdf, output_pdf, password)

if __name__ == '__main__':
    main()
    