import argparse
import subprocess
import os
import glob

'''
Requirements
sudo apt-get install texlive-latex-extra
'''

# Your cover letter specific includes
template_path = 'cover_letter_template.tex'
name = 'Geoffrey Bian'

# Script specific default job information
companyname = 'Rivian'
jobtitle = 'Softare Engineer Intern'

def replace_vars_in_latex(template_path, output_path, replacements):
    with open(template_path, 'r') as file: 
        latex_content = file.read()

    for current, replacement in replacements.items():
        latex_content = latex_content.replace(current, replacement)
    
    with open(output_path, 'w') as file:
        file.write(latex_content)

def compile_latex_to_pdf(tex_file):
    directory, base = os.path.split(tex_file)

    try:
        os.chdir(directory)
        subprocess.run(['pdflatex', base], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Problematic: {e}")
    finally:
        os.chdir(os.path.dirname(__file__))
    
def delete_non_pdf_files(directory):
    if not os.path.isdir(directory):
        print("it's over")
        return

    files = glob.glob(os.path.join(directory, '*'))

    for file_path in files:
        if os.path.isfile(file_path) and not file_path.lower().endswith('pdf'):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"e")

# Script starts here
parser = argparse.ArgumentParser(description="Geoffrey's Cover Letter argument parser")
parser.add_argument('--companyname', type=str, default=companyname)
parser.add_argument('--nameofjob', type=str, default=jobtitle)
args = parser.parse_args()

if not os.path.exists(args.companyname):
    os.makedirs(args.companyname)

output_path = f'{args.companyname}/Cover_Letter_{args.companyname}_{name.replace(" ", "_")}.tex'

replacements = {
    'COMPANY_NAME_TO_REPLACE': f'{args.companyname}',
    'NAME_OF_JOB_TO_REPLACE': f'{args.nameofjob}'
}

replace_vars_in_latex(template_path, output_path, replacements)
compile_latex_to_pdf(output_path)
delete_non_pdf_files(args.companyname)