import os, requests
 
def formula_as_file( formula, file, negate=False ):
    tfile = file
    if negate:
        tfile = 'tmp.png'
    r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{300} \huge %s' % formula )
    f = open( tfile, 'wb' )
    f.write( r.content )
    f.close()
    if negate:
        os.system( 'convert tmp.png -channel RGB -negate -colorspace rgb %s' %file )

formula_as_file( r"(F/P, i, N) = (1+i)^N", "Eq_FP.png")
formula_as_file(r"(P/F, i, N) = \frac{1}{(1+i)^N}", "Eq_PF.png")
formula_as_file(r"(A/F, i, N) = \frac{i}{(1+i)^N-1}", "Eq_AF.png")
formula_as_file(r"(F/A, i, N) = \frac{(1+i)^N-1}{i}", "Eq_FA.png")
formula_as_file(r"(A/P, i, N) = \frac{i(1+i)^N}{(1+i)^N-1}", "Eq_AP.png")
formula_as_file(r"(P/A, i, N) = \frac{(1+i)^N-1}{i(1+i)^N}", "Eq_PA.png")
formula_as_file(r"(A/G, i, N) = \frac{1}{i}-\frac{N}{i(1+i)^N-1}", "Eq_AG.png")
formula_as_file(r"(P/A, g, i, N) = \frac{(1+i_0)^N-1}{i_0(1+i_0)^N}\left ( \frac{1}{1+g} \right )", "Eq_PAg.png")
formula_as_file( r"(i\_0, i, N) = \frac{1+i}{1+g}-1", "Eq_i_0.png")
formula_as_file( r"(i\_e, i, N) = \left ( 1+\frac{r}{m} \right )^k-1", "Eq_i_e.png")
