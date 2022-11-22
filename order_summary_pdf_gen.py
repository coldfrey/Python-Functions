from calendar import day_abbr
from ctypes import alignment
import json
from sys import int_info
from fpdf import FPDF
from CommerceQueries import addOrdersToDict 

class CustomPDF(FPDF):

    with open("API_data.json", "r") as read_file:
        data = json.load(read_file)
    
    def header(self):
        # Set up a logo on the right side of the page
        
        self.set_font('Arial', 'I' , 14)
        self.cell(80)
        self.cell(30, 10, 'Captain App Report', 0, 0, 'C')
        self.ln(20)
        self.image('uncommonLogo.png', 10, 8, 33)

        # Line break
        self.ln(20)

    def content(self, data):                           
        #for each order in the data, add a cell with the order number and status
        # for order in data:
        #     # ids.append(order)
        #     self.cell(200, 10, txt = order, ln = 3, align = 'L')
        #     self.cell(200, 10, txt = data[order]["Status"], ln = 3, align = 'L')
        self.cell(200, 10, txt = "Purchase Breakdown:", ln = 2, align = 'C')
        self.ln(10)
        self.set_font('Arial', '', 12)
        self.cell(30, 10, 'Order ID', 'C')      
        self.cell(20)
        self.cell(30, 10, 'Customer Email', 'C')
        self.cell(20)
        self.cell(30, 10, 'Date', 'C')
        self.cell(20)
        self.cell(30, 10, 'Total Price', 'C')
        self.ln(10)
        #list the first order and all of its information    
        for order in data:
            self.cell(30, 10, txt = order, align = 'C')
            self.cell(20)
            self.cell(30, 10, txt = data[order]["CustomerEmail"], align = 'C')
            self.cell(20)
            # date is the first 10 characters of the 'OrderDate' key
            date = data[order]["OrderDate"][:10]
            self.cell(30, 10, txt = date, align = 'C')
            self.cell(20)
            self.cell(30, 10, txt = data[order]["TotalPrice"], align = 'C')
            self.ln(10)

        # add page per order with order details in table format

        for order in data:
            self.add_page()
            self.cell(50, 10, 'Shipping Address:', 'C')
            # Shipping Address is the value of the 'BillingInfo' key and needs to have unicode characters removed
            shippingAddress = data[order]["ShippingInfo"].encode('ascii', 'ignore').decode('ascii')
            #split the address by comma into a list of lines
            addressLines = shippingAddress.split(',')
            # add each line to a cell
            for line in addressLines:
                self.ln(5)
                self.cell(100, 10, txt = line, align = 'l')
            self.ln(10)
            self.cell(50 , 10, 'Email:', 'C')
            self.cell(100, 10, txt = data[order]["CustomerEmail"], align = 'l')
            self.ln(10)
            self.cell(50 , 10, 'Order ID:', 'C')
            self.cell(100, 10, txt = order, align = 'l')
            self.ln(10)
            
            
            self.cell(200, 10, txt = "Order Details:", ln = 2, align = 'C')
            self.ln(10)
            self.cell(30, 10, 'Unit Description', 'l')      
            self.cell(20)
            self.cell(30, 10, 'Unit Quantity', 'C')
            self.cell(20)
            self.cell(30, 10, 'Unit Price', 't')
            self.cell(20)
            self.cell(30, 10, 'Total', 't')
            self.ln(10)
            for unit in data[order]["UnitDescription"]:
                self.cell(30, 10, txt = unit["unit_description"], align = 'l')
                self.cell(20)
                self.cell(30, 10, txt = str(unit["quantity"]), align = 'C')
                self.cell(20)
                self.cell(30, 10, txt = unit["unit_price"], align = 'R')
                self.cell(20)
                self.cell(30, 10, txt = unit["total_price"], align = 'R')
                self.ln(10)
            self.ln(10)
            self.cell(200, 10, txt = "Total: " + data[order]["TotalPrice"], ln = 2, align = 'R')
            self.cell(10)

    def footer(self):
        self.set_y(-10)
        
        self.set_font('Arial', 'I', 8)
        
        # Add a page number
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')
        
def create_pdf(pdf_path):
    pdf = CustomPDF()
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.set_font('Times', '', 12)
    pdf.add_page()
    pdf.content(pdf.data)
    # line_no = 1
    # for i in range(50):
    #     pdf.cell(0, 10, txt="Line #{}".format(line_no), ln=1)
    #     line_no += 1
    
    pdf.output(pdf_path)
    
if __name__ == '__main__':
    create_pdf('CA-report.pdf')