import traceback

def write_to_HPL_dat(file_name, new_param, core_count):
    try:
        with open('HPL.dat', 'w') as file:
            file.write("HPLinpack benchmark input file\n")
            file.write("Innovative Computing Laboratory, University of Tennessee\n")
            file.write("HPL.out      output file name (if any)\n")
            file.write("6            device out (6=stdout,7=stderr,file)\n")
            file.write("1            # of problems sizes (N)\n")
            file.write(f"{new_param['Ns']}        Ns\n")
            file.write("1            # of NBs\n")
            file.write(f"{new_param['NBs']}        NBs\n")
            file.write(f"{new_param['PMAP']}            PMAP process mapping (0=Row-,1=Column-major)\n")
            file.write("1            # of process grids (P x Q)\n")
            file.write(f"{core_count//new_param['Qs']}          Ps\n")
            file.write(f"{new_param['Qs']}          Qs\n")
            file.write("-1         threshold\n")
            file.write("1           # of panel fact\n")
            file.write(f"{new_param['PFACTs']}            PFACTs (0=left, 1=Crout, 2=Right)\n")
            file.write("1            # of recursive stopping criterium\n")
            file.write(f"{new_param['NBMINs']}            NBMINs\n")
            file.write("1           # of panels in recursion\n")
            file.write(f"{new_param['NDIVs']}            NDIVs\n")
            file.write("1            # of recursive panel fact.\n")
            file.write(f"{new_param['RFACTs']}            RFACTs (0=left, 1=Crout, 2=Right)\n")
            file.write("1            # of broadcast\n")
            file.write(f"{new_param['BCASTs']}            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)\n")
            file.write("1            # of lookahead depth\n")
            file.write(f"{new_param['DEPTHs']}            DEPTHs (>=0)\n")
            file.write(f"{new_param['SWAP']}            SWAP (0=bin-exch,1=long,2=mix)\n")
            file.write("64           swapping threshold\n")
            file.write(f"{new_param['L1']}            L1 in (0=transposed,1=no-transposed) form\n")
            file.write(f"{new_param['U']}            U  in (0=transposed,1=no-transposed) form\n")
            file.write(f"{new_param['Equilibration']}            Equilibration (0=no,1=yes)\n")
            file.write("8            memory alignment in double (> 0)\n")
        return "文件写入成功"
    except Exception as e:
        traceback.print_exc()
        return f"写入文件时发生错误: {str(e)}"