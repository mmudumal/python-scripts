from datetime import timedelta,datetime, date, time
import datetime
import os,sys,subprocess,re
import fnmatch


Hostname =raw_input("Enter the hostname:  ")
From_Date=raw_input("Enter the from date:  ")
To_Date=raw_input("Enter the to date:  ")
Search_String=raw_input("Enter the Search String: ")

Email='mallikarjun.mudumali@oracle.com'
Current_Time= datetime.datetime.now().strftime("_%Y-%m-%d-%H-%M-%S")
FileName='/tmp/pblogs'+'_'+Hostname+Current_Time
Dc_Command= "/usr/local/git/bin/host-group -Field=data_center " + Hostname



class color:
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   PURPLE = '\033[95m'
   DARKCYAN = '\033[36m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def get_dc_name():
    Get_DcName=subprocess.Popen([Dc_Command],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    DcName=Get_DcName.stdout.readlines()
    return DcName[0]

pb_files_list=[]
def get_pbfiles_list():
    Search_Start=datetime.datetime.strptime(From_Date, '%d/%m/%Y')
    Search_End=datetime.datetime.strptime(To_Date, '%d/%m/%Y')
    delta=Search_End - Search_Start
    
    for i in range(delta.days + 1):
        Search_Date=str(Search_Start+timedelta(days=i))[0:10]
        Search_Path=os.path.join(Mount_point,Search_Date)
        if os.path.isdir(Search_Path):
            print color.UNDERLINE + '\n\n' + "below pbfiles are found for date {}".format(Search_Date) + color.END
            for file in os.listdir(Search_Path):
                if fnmatch.fnmatch(file, str('*'+Hostname+'*')):
                    File_Path=os.path.join(Search_Path,file)
                    print File_Path 
                    pb_files_list.append(File_Path)

def gen_pb_files():
    d_file=open(FileName,'a')
    for file in pb_files_list:
        d_file.write('\n' + file + '\n')
        pboutput=subprocess.Popen(["pbreplay", "-o", file],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result=pboutput.stdout.readlines()
        output=str("\n".join(result)).rstrip('\n')
        d_file.write(output)
        d_file.write('\n' + '==' * 64 + '\n')
    d_file.close()


if __name__=='__main__':
    DataCenter=get_dc_name()
    print  color.BOLD + '\n\n' + "The server is hosted in Data center: ",DataCenter + color.END
    mountpoint={'adc':'ADC_new', 'lldc':'LLG_new','sldc':'SLDC', 'rmdc':'RMDC','trdc':'TRDC','sydc':'SYDC','cgydc':'CGYDC','tvp':'TVP','epdc':'EPDC'}
    Mount_point=os.path.join('/var/log/pb_logs',mountpoint.get(DataCenter),'archive')
        
    get_pbfiles_list()
    gen_pb_files()
    

    with open(FileName,'r')as inp:
        for line in inp.readlines():
           if not re.match(r'^\s*$', line):
              if "su from" in line:
                 print color.BOLD + color.GREEN + line.rstrip('\n') + color.END
              elif "/var/log/pb_logs" in line:
                 print color.BOLD + color.GREEN + line.rstrip('\n') + color.END
              elif "=======================================" in line:
                 print color.PURPLE + line.rstrip('\n') + color.END
              elif Search_String in line:
                 print color.BOLD + color.UNDERLINE + color.RED + line.rstrip('\n') + color.END
              else:
                 print line.rstrip('\n')
    print "Logs are saved in",FileName
