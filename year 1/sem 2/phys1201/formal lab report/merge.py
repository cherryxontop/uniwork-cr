from pypdf import PdfWriter

def merge_pdfs():
   merger = PdfWriter()
   merger.append("integdec.pdf")
   merger.append("phys_formreport.pdf")
   merger.write("rep.pdf")
   merger.close()
   print("merged!")

if __name__ == "__main__":
  merge_pdfs()