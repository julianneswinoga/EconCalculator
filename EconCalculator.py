import sys, webbrowser
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
        self.k = ""
        self.A = ""
        self.g = ""
        self.formulaText = ""

    def parseVariable(self, var, varStr):
        if (self.formulaText.find(varStr) != -1 and varStr == "i"):
            try:
                if (self.formulaText[self.formulaText.find(varStr)+1] == "_"):
                    return
            except:
                pass
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
            
    def evaluateFormula(self, equationNotation, actualEquation):        
        start = self.formulaText.find("(" + equationNotation)
        if (start == -1):
            return
        end = self.formulaText.find(")", start)        
        args = self.formulaText[start:end].split(",")

        self.formulaText = self.formulaText[:start] + actualEquation + self.formulaText[end+1:]
        
        for a, arg in enumerate(args[1:]): #Skip the first element because it's the equation
            self.formulaText = self.formulaText.replace("arg_"+str(a+1), str(arg).strip())
            print "Replaced arg_"+str(a+1)+" with "+str(arg)
    
    def replaceFormulas(self):
        self.evaluateFormula("i_0", "(((1+arg_1)/(1+arg_2))-1)")
        self.evaluateFormula("i_e", "((1+(arg_1/arg_2))^arg_3-1)")
        
        self.evaluateFormula("F/P", "((1+arg_1)^arg_2)")
        self.evaluateFormula("P/F", "(1/((1+arg_1)^arg_2))")
        self.evaluateFormula("A/F", "(1/(((1+arg_1)^arg_1)-1))")
        self.evaluateFormula("F/A", "(((1+arg_1)^arg_2-1)/arg_1)")
        self.evaluateFormula("A/P", "((arg_1*(1+arg_1)^arg_2)/((1+arg_1)^arg_2-1))")
        self.evaluateFormula("P/A", "(((1+arg_1)^arg_2-1)/(arg_1*(1+arg_1)^arg_2))")
        self.evaluateFormula("A/G", "((1/arg_1)-(arg_2/((1+arg_1)^arg_2-1)))")
        self.evaluateFormula("P/A", "((((1+(i_0))^arg_3-1)/((i_0)*(1+(i_0))^arg_3))*(1/(1+arg_1)))")
        
    def parseFormula(self):
        preFormula = self.formulaText
        self.replaceFormulas()
        
        self.parseAgain = True
        while (self.parseAgain and preFormula != self.formulaText):
            preFormula = self.formulaText
            self.parseAgain = False
            self.parseVariable(self.P, "P")
            self.parseVariable(self.i, "i")
            self.parseVariable(self.r, "r")
            self.parseVariable(self.m, "m")
            self.parseVariable(self.k, "k")
            self.parseVariable(self.N, "N")
            self.parseVariable(self.A, "A")
            self.parseVariable(self.g, "g")
            print preFormula + " -> " + self.formulaText

        try:
            rtn = parser.parse(self.formulaText).simplify({}).toString()
        except:
            print "Could not simplify"
            try:
                rtn = parser.parse(self.formulaText).evaluate({})
                print "Evaluated: " + str(rtn)
            except:
                print "Could not evaluate"
        try:
            return str(rtn)
        except:
            return "Error parsing formula (" + self.formulaText + ")"

currFormula = Formula() # Create instance of formula class

class EngEconWindow:
    def __init__(self):
        self.gladefile = "GUI/EngEcon.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.scaleImages(0.15)
        self.window.show()
        
        settings = gtk.settings_get_default()
        settings.props.gtk_button_images = True

    def scaleImage(self, scale, fileName):
        pixbuf = gtk.gdk.pixbuf_new_from_file("GUI/" + fileName + ".png")
        scaled_buf = pixbuf.scale_simple(int(pixbuf.get_width()*scale), int(pixbuf.get_height()*scale), gtk.gdk.INTERP_BILINEAR)
        self.builder.get_object("Img_" + fileName).set_from_pixbuf(scaled_buf)
        self.builder.get_object("Bttn_" + fileName).set_image(self.builder.get_object("Img_" + fileName))
        self.builder.get_object("Bttn_" + fileName).set_label("")

    def scaleImages(self, scale):
        imgFilenames = ["Eq_PF", "Eq_FP", "Eq_AF", "Eq_FA", "Eq_AP", "Eq_PA", "Eq_AG", "Eq_PAg", "Eq_i_0", "Eq_i_e"]
        for imgName in imgFilenames:
            self.scaleImage(scale, imgName)
    def formulaButtonClicked(self, equation):
        textBox = self.builder.get_object("FormulaInput").get_text()
        formula = equation
        if (textBox != ""):
            self.builder.get_object("FormulaInput").set_text(textBox + (formula if isCharInString(textBox[-1], "+-*/^") else "+" + formula))
        else:
            self.builder.get_object("FormulaInput").set_text(formula)

    def on_BttnGenFormula_clicked(self, object, data=None):
        currFormula.P = self.builder.get_object("Txt_VarP").get_text()
        currFormula.i = self.builder.get_object("Txt_Vari").get_text()
        currFormula.r = self.builder.get_object("Txt_Varr").get_text()
        currFormula.m = self.builder.get_object("Txt_Varm").get_text()
        currFormula.k = self.builder.get_object("Txt_Vark").get_text()
        currFormula.N = self.builder.get_object("Txt_VarN").get_text()
        currFormula.A = self.builder.get_object("Txt_VarA").get_text()
        currFormula.g = self.builder.get_object("Txt_Varg").get_text()
        
        currFormula.formulaText = self.builder.get_object("FormulaInput").get_text()
        self.builder.get_object("FormulaOutput").set_text(currFormula.formulaText+"="+currFormula.parseFormula())
    
    def on_BttnClearVars_clicked(self, object, data=None):
        self.builder.get_object("Txt_VarP").set_text("")
        self.builder.get_object("Txt_Vari").set_text("")
        self.builder.get_object("Txt_Varr").set_text("")
        self.builder.get_object("Txt_Varm").set_text("")
        self.builder.get_object("Txt_Vark").set_text("")
        self.builder.get_object("Txt_VarN").set_text("")
        self.builder.get_object("Txt_VarA").set_text("")
        self.builder.get_object("Txt_Varg").set_text("")
        currFormula.clearAll() 
        print "Variables Cleared"

    def on_BttnClearFormula_clicked(self, object, data=None):
        self.builder.get_object("FormulaInput").set_text("")
        print "Formula cleared"

    def on_Bttn_Eq_FP_clicked(self, object, data=None):
        self.formulaButtonClicked("(F/P, i, N)")

    def on_Bttn_Eq_PF_clicked(self, object, data=None):
        self.formulaButtonClicked("(P/F, i, N)")

    def on_Bttn_Eq_AF_clicked(self, object, data=None):
        self.formulaButtonClicked("(A/F, i, N)")

    def on_Bttn_Eq_FA_clicked(self, object, data=None):
        self.formulaButtonClicked("(F/A, i, N)")

    def on_Bttn_Eq_AP_clicked(self, object, data=None):
        self.formulaButtonClicked("(A/P, i, N)")

    def on_Bttn_Eq_PA_clicked(self, object, data=None):
        self.formulaButtonClicked("(P/A, i, N)")

    def on_Bttn_Eq_AG_clicked(self, object, data=None):
        self.formulaButtonClicked("(A/G, i, N)")

    def on_Bttn_Eq_PAg_clicked(self, object, data=None):
        self.formulaButtonClicked("(P/A, g, i, N)")

    def on_Bttn_Eq_i_0_clicked(self, object, data=None):
        self.formulaButtonClicked("(i_0, i, g)")

    def on_Bttn_Eq_i_e_clicked(self, object, data=None):
        self.formulaButtonClicked("(i_e, r, m, k)")

    def on_Bttn_GithubLink_clicked(self, object, data=None):
        webbrowser.open("https://github.com/camca123/EconCalculator")

    def saveGeneric(self, equationNumber):
        f = open("formula" + str(equationNumber), "w")
        f.write(self.builder.get_object("FormulaInput").get_text())
        f.close()

    def loadGeneric(self, equationNumber):
        if (self.builder.get_object("FormulaInput").get_text() == ""): #Only overwrite if the formula box is empty
            f = open("formula" + str(equationNumber), "r")
            self.builder.get_object("FormulaInput").set_text(f.read())
            f.close()
        else:
            pass
            
    def on_Bttn_Save1_clicked(self, object, data=None):
        self.saveGeneric(1)
    def on_Bttn_Save2_clicked(self, object, data=None):
        self.saveGeneric(2)
    def on_Bttn_Save3_clicked(self, object, data=None):
        self.saveGeneric(3)
    def on_Bttn_Save4_clicked(self, object, data=None):
        self.saveGeneric(4)

    def on_Bttn_Load1_clicked(self, object, data=None):
        self.loadGeneric(1)
    def on_Bttn_Load2_clicked(self, object, data=None):
        self.loadGeneric(2)
    def on_Bttn_Load3_clicked(self, object, data=None):
        self.loadGeneric(3)
    def on_Bttn_Load4_clicked(self, object, data=None):
        self.loadGeneric(4)
        
    def on_window1_destroy(self, object, data=None):
        gtk.main_quit()
        
def isCharInString(char, string):
    for c in string:
        if (char == c):
            return True
    return False

if __name__ == "__main__":
  main = EngEconWindow()
  gtk.main()
