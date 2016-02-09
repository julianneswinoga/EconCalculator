import sys
from py_expression_eval import Parser
try:
    import pygtk
    pygtk.require('2.0')
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    print('GTK not available')
    sys.exit(1)
parser = Parser()

class Formula:    
    def __init__(self):
        self.parseAgain = True
        self.clearAll()
        
    def clearAll(self):
        self.P = ""
        self.i = ""
        self.N = ""
        self.r = ""
        self.m = ""
        self.A = ""
        self.formulaText = ""

    def parseVariable(self, var, varStr):
        try:
            if (var[-1] == "%"):
                var = float(var[0:len(var)-1])/100.0
            else:
                var = float(var) # Try to convert the variable to a float
        except:
            pass # The variable is an unparsable expression
        if (var == ""): # If the textbox is left blank
            var = varStr # Substutute it for the default variable
        print var
        self.formulaText = self.formulaText.replace(varStr, str(var)) # Replace all the variables with whatever happened above (float or text)
        if (self.formulaText.find(varStr) != -1): # If we can still find the variable, we need to iterate again
            self.parseAgain = True
        
    def parseFormula(self):
        self.formulaText = self.formulaText.replace("(F/P)", "((1+i)^N)")
        self.formulaText = self.formulaText.replace("(P/F)", "(1/((1+i)^N))")
        self.formulaText = self.formulaText.replace("(A/F)", "(1/(((1+i)^N)-1))")
        self.formulaText = self.formulaText.replace("(F/A)", "(((1+i)^N-1)/i)")
        self.formulaText = self.formulaText.replace("(A/P)", "((i*(1+i)^N)/((1+i)^N-1))")

        self.parseAgain = True
        preFormula = ""
        while (self.parseAgain and preFormula != self.formulaText):
            preFormula = self.formulaText
            self.parseAgain = False
            self.parseVariable(self.P, "P")
            self.parseVariable(self.i, "i")
            self.parseVariable(self.r, "r")
            self.parseVariable(self.m, "m")
            self.parseVariable(self.N, "N")
            self.parseVariable(self.N, "A")
            print preFormula + " -> " + self.formulaText

        try:
            rtn = parser.parse(self.formulaText).simplify({}).toString()
            print "Could not simplify"
        except:
            try:
                rtn = parser.parse(self.formulaText).evaluate({})
                print "Evaluated: " + str(rtn)
            except:
                print "Could not evaluate"
        return str(rtn)

currFormula = Formula()

class EngEconWindow:
    def __init__(self):
        self.gladefile = "GUI/EngEcon.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.show()

    def on_BttnGenFormula_clicked(self, object, data=None):
        currFormula.P = self.builder.get_object("Txt_VarP").get_text()
        currFormula.i = self.builder.get_object("Txt_Vari").get_text()
        currFormula.r = self.builder.get_object("Txt_Varr").get_text()
        currFormula.m = self.builder.get_object("Txt_Varm").get_text()
        currFormula.N = self.builder.get_object("Txt_VarN").get_text()
        currFormula.A = self.builder.get_object("Txt_VarA").get_text()
        
        currFormula.formulaText = self.builder.get_object("FormulaInput").get_text()
        self.builder.get_object("FormulaOutput").set_text(currFormula.formulaText+"="+currFormula.parseFormula())
    
    def on_BttnClearVars_clicked(self, object, data=None):
        self.builder.get_object("Txt_VarP").set_text("")
        self.builder.get_object("Txt_Vari").set_text("")
        self.builder.get_object("Txt_VarN").set_text("")
        
        currFormula.clearAll() 
        print "Clear Variables"
    def on_window1_destroy(self, object, data=None):
        print "Quit with cancel"
        gtk.main_quit()
        

if __name__ == "__main__":
  main = EngEconWindow()
  gtk.main()
