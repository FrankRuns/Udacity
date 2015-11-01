import csv

def parse_file(datafile):
    data = []
    with open(datafile, "rU") as f:
        reed = csv.DictReader(f)
        for line in reed:
            data.append(line)
    return data

# data = ['Title,Released,Label,UK Chart Position,US Chart Position,BPI Certification,RIAA Certification\rPlease Please Me,22-Mar-63,Parlophone(UK),1,-,Gold,Platinum\rWith the Beatles,22-Nov-63,Parlophone(UK),1,-,Platinum,Gold\rBeatlemania! With the Beatles,25-Nov-63,Capitol(CAN),-,-,,\rIntroducing... The Beatles,10-Jan-64,Vee-Jay(US),-,2,,\rMeet the Beatles!,20-Jan-64,Capitol(US),-,1,,5xPlatinum\rTwist and Shout,3-Feb-64,Capitol(CAN),-,-,,\rThe Beatles\' Second Album,10-Apr-64,Capitol(US),-,1,,2xPlatinum\rThe Beatles\' Long Tall Sally,11-May-64,Capitol(CAN),-,-,,\rA Hard Day\'s Night,26-Jun-64,United Artists(US)[C],-,1,,4xPlatinum\r,10-Jul-64,Parlophone(UK),1,-,Gold,\rSomething New,20-Jul-64,Capitol(US),-,2,,Platinum\rBeatles for Sale,4-Dec-64,Parlophone(UK),1,-,Gold,Platinum\rBeatles \'65,15-Dec-64,Capitol(US),-,1,,3xPlatinum\rBeatles VI,14-Jun-65,"Parlophone(NZ), Capitol(US)",-,1,,Platinum\rHelp!,6-Aug-65,Parlophone(UK),1,-,Platinum,\r,13-Aug-65,Capitol(US)[C],-,1,,3xPlatinum\rRubber Soul,3-Dec-65,Parlophone(UK),1,-,Platinum,\r,6-Dec-65,Capitol(US)[C],-,1,,6xPlatinum\rYesterday and Today,15-Jun-66,Capitol(US),-,1,,2xPlatinum\rRevolver,5-Aug-66,Parlophone(UK),1,-,Platinum,\r,8-Aug-66,Capitol(US)[C],-,1,,5xPlatinum\rSgt. Pepper\'s Lonely Hearts Club Band,1-Jun-67,"Parlophone(UK), Capitol(US)",1,1,3xPlatinum,11xPlatinum\rMagical Mystery Tour,27-Nov-67,"Parlophone(UK), Capitol(US)",31[D],1,Platinum,6xPlatinum\rThe Beatles,22-Nov-68,"Apple(UK), Capitol(US)",1,1,Platinum,19xPlatinum\rYellow Submarine,13-Jan-69,"Apple(UK), Capitol(US)",3,2,Silver,Platinum\rAbbey Road,26-Sep-69,"Apple(UK), Capitol(US)",1,1,2xPlatinum,12xPlatinum\rLet It Be,8-May-70,"Apple(UK),United Artists(US)",1,1,Gold,4xPlatinum']

def test():
    # a simple test of your implemetation
    d = parse_file('beatles-diskography.csv')
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22-Mar-63', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10-Jul-64', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

    
test()