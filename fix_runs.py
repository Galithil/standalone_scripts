import argparse
import os

from lxml import etree
from genologics.entities import *
from genologics.lims import *
from genologics.config import BASEURI, USERNAME, PASSWORD


def main(args):
    lims= Lims(BASEURI, USERNAME, PASSWORD)
    pro=Process(lims, id=args.pid)
    rp=os.path.join(args.folder, "runParameters.xml")
    with open(rp, 'r') as rpf:
        d=etree.parse(rpf)
        if d.findall(".//WorkFlowType")[0].text == "DUALINDEX":
            pro.udf["Run Type"]="Paired End Dual Indexing Run"

        runid=d.findall(".//RunID")[0].text
        fcid=runid.split('_')[-1]
        pro.udf["Run ID"]=runid
        pro.udf["Flow Cell ID"]=fcid
        
        cycles=int(d.findall(".//Read1")[0].text)
        pro.udf["Read 1 Cycles"]=cycles
        pro.udf["Index 1 Read Cycles"]=int(d.findall(".//IndexRead1")[0].text)
        pro.udf["Index 2 Read Cycles"]=int(d.findall(".//IndexRead2")[0].text)

        if d.findall(".//IndexRead2")[0].text != "0":
            pro.udf["Read 2 Cycles"]=int(d.findall(".//Read2")[0].text)

        pro.udf["Output Folder"]=d.findall(".//OutputFolder")[0].text

        kit=d.findall(".//Sbs")[0].text + " ({} cycles)".format(int(cycles)-1)
        pro.udf["SBS Kit Type"] =kit

        pro.udf["SBS Kit Lot #"]=d.findall(".//SbsReagentKit")[0].findall('ID')[0].text

        pro.udf["Flow Cell Version"]=d.findall(".//Flowcell")[0].text
        pro.udf["Flow Cell Position"]=d.findall(".//FCPosition")[0].text
        pro.udf["Experiment Name"]=d.findall(".//ExperimentName")[0].text

        pro.put()



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", dest="folder")
    parser.add_argument("-p", "--pid", dest="pid")
    args = parser.parse_args()
    main(args)
