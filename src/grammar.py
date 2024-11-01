instant_grammar = """
?program: stmt_list                 -> prog
        | exp                        -> expression_stmt

?stmt_list: stmt (";" stmt)*

?stmt: IDENT "=" exp                 -> assignment
     | exp                           -> expression_stmt

?exp: exp "+" term                   -> exp_add
     | exp "-" term                  -> exp_sub
     | term                          -> term_expr

?term: term "*" factor               -> exp_mul
     | term "/" factor               -> exp_div
     | factor                        -> factor_expr

?factor: atom
       | "(" exp ")"                 -> exp_paren

?atom: INTEGER                       -> exp_lit
     | IDENT                         -> exp_var

%import common.CNAME -> IDENT        
%import common.INT   -> INTEGER      
%import common.WS_INLINE

%ignore WS_INLINE
"""
