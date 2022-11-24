from calendar import day_abbr
from ctypes import alignment
import json
from sys import int_info
from fpdf import FPDF
from retrieveSpecifcOrder import retrieveSpecificOrder

from getAuth import authToken

class CustomPDF(FPDF):

    def header(self):
        # Set up a logo on the right side of the page
        
        self.set_font('Arial', 'I' , 14)
        self.cell(80)
        self.cell(30, 10, 'Captain App Report', 0, 0, 'C')
        self.ln(20)
        self.image('uncommonLogo.png', 10, 8, 33)
        self.data = ''
        # Line break
        self.ln(20)

    # Function creates new field for refactored data
    def refactorUnitDescription(self, units):
        import re

        rep = {'\(2XS\)': '1',
               '\(XS\)': '2', 
               '\(S\)': '3',
               '\(M\)': '4',
               '\(L\)': '5',
               '\(XL\)': '6',
               '\(2XL\)': '7',
               '\(3XL\)': '8',
               '\(6\)': '1',
               '\(8\)': '2',
               '\(10\)': '3',
               '\(12\)': '4',
               '\(14\)': '5',
               '\(16\)': '6',}
    
        for unit in units:
            sortVariable = unit["unit_description"].upper()
            for key, value in rep.items():
                sortVariable = re.sub(key, value, sortVariable)
            unit["sortVariable"] = sortVariable
        return units
    


    def content(self, orderID, data):    

        self.cell(50, 10, 'Shipping Address:', 'C')
        # Shipping Address is the value of the 'BillingInfo' key and needs to have unicode characters removed
        shippingAddress = data["ShippingInfo"].encode('ascii', 'ignore').decode('ascii')
        #split the address by comma into a list of lines
        addressLines = shippingAddress.split(',')
        # add each line to a cell
        for line in addressLines:
            self.ln(5)
            self.cell(100, 10, txt = line, align = 'l')
        self.ln(10)
        self.cell(50 , 10, 'Email:', 'C')
        self.cell(100, 10, txt = data["CustomerEmail"], align = 'l')
        self.ln(10)
        self.cell(50 , 10, 'Order ID:', 'C')
        self.cell(100, 10, txt = orderID, align = 'l')
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

        units = data["UnitDescription"]
        units = self.refactorUnitDescription(units)
        units.sort(key = lambda x: x["sortVariable"])

        for unit in units:
            # self.cell(30, 10, txt = unit["sortVariable"], align = 'l')
            # self.cell(20)
            self.cell(30, 10, txt = unit["unit_description"], align = 'l')
            self.cell(20)
            self.cell(30, 10, txt = str(unit["quantity"]), align = 'C')
            self.cell(20)
            self.cell(30, 10, txt = unit["unit_price"], align = 'R')
            self.cell(20)
            self.cell(30, 10, txt = unit["total_price"], align = 'R')
            self.ln(10)
        self.ln(10)
        self.cell(200, 10, txt = "Total: " + data["TotalPrice"], ln = 2, align = 'R')
        self.cell(10)

    def footer(self):
        self.set_y(-10)
        
        self.set_font('Arial', 'I', 8)
        
        # Add a page number
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')
        
def create_pdf(orderID, subdomain, authToken):
    pdf = CustomPDF()
    data = retrieveSpecificOrder(orderID, subdomain, authToken)
    print(data["OrderDate"])
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.set_font('Times', '', 12)
    pdf.add_page()
    pdf.content(orderID, data)
    
    pdf.output('/tmp/OrderSummary_' + orderID + '.pdf')
    
if __name__ == '__main__':
    create_pdf(orderID="PKaehVzKaL", subdomain='uncommon', authToken=authToken)