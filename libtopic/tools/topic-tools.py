#-*- coding: utf-8 -*- 
#!/usr/bin/env python
"""Topic tools

Syntax : topic-tools toolname [args]

Available tools:
csv_to_django_fixture [source_file] [target_model] : convert a csv file to a django fixture


For help :
topic-tools (-h|--help)

"""
import os
import sys
import getopt
import traceback
from django.utils import simplejson
from libtopic.io import get_lines_from_file

def csv_to_django_fixture(args):
    # Instructions pour le format du fichier d'entrée
    # 1) Le fichier doit être encodé en UTF8
    # 2) La première ligne du fichier doit contenir les noms de colonne
    # 3) Par défaut, les valeurs sont considérées comme des 'string' sauf si un type différent est spécifié dans le nom de la colonne (ex : "category[int]")
    # 4) Pour qu'une colonne soit ignorée, la nommer : <ignore> 
    print " == csv_to_django_fixture =="
    if len(args)!=3:
        print "Missing argument after 'csv_to_django_fixture'. See -h for help"
    else:
        source_file = args[1]
        target_model = args[2]
        lines = get_lines_from_file(source_file)   
        print "Source file : %s. %s line(s) read" % (source_file,len(lines))
        print "Target model :" + target_model
        header_line = lines [0]
        columns = header_line.split(";")
        column_names = []
        column_types = []
        print "Columns :"
        for column in columns:
            column_name_tokens = column.split("[")
            column_name = column_name_tokens[0]
            column_names.append(column_name)
            column_type = "str"
            if len(column_name_tokens)>1:
                column_type = column_name_tokens[1].split("]")[0]                            
            column_types.append(column_type)
            print "%s (%s)" % (column_name,column_type)                
        results = []
        line_cpt = 0
        process_ok = True
        for line in lines[1:]:
            line_cpt = line_cpt + 1
            try:
                tokens = line.split(";")
                line_dict = {}
                fields_dict = {}
                cpt = 1
                for token in tokens[1:]:
                    column_name = column_names[cpt]
                    if column_name != "<ignore>":
                        if len(token)>0:
                            if column_types[cpt]=="str":
                                fields_dict[column_name] = token
                            elif column_types[cpt]=="int":
                                fields_dict[column_name] = int(token)
                            else:
                                raise str("Unknown column type : %" %column_types[cpt])
                    cpt = cpt + 1
                line_dict["model"]    = target_model
                line_dict["pk"]       = int(tokens[0])
                line_dict["fields"]   = fields_dict
                results.append(line_dict)
            except:
                process_ok = False
                traceback.print_exc()   # Imprime le message d'erreur                            
                print "Could not process the line #%s : '%s'" % (line_cpt,line)
                if len(line.strip())==0:
                    print "Is this an empty line ?"                
        # Serialize to JSON
        if process_ok:
            content = simplejson.dumps(results)
            path_tokens = os.path.split(source_file)
            output_file = "".join(path_tokens[:len(path_tokens)-1])
            output_file += "\\"
            output_file += path_tokens[len(path_tokens)-1]
            output_file += ".json"        
            print "Writing output file : %s" % output_file
            f = open(output_file , "w")
            f.write(content)
            f.close()        
            print "Done !"
        else:
            print "Failed !"
                                                                       
def main():
    # parse command line options
    import_operation = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h,a", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)        
    # process arguments
    if len(args)<1:
        print "Missing argument: filename. See -h for help"
        sys.exit(0)
    toolname = args[0]        
    if toolname:
        if toolname == "csv_to_django_fixture":
            return csv_to_django_fixture(args)
        else:
            print "Unknown toolname. See -h for help"
    else:
        print "No toolname specified. See -h for help"

if __name__ == "__main__":
    main()
