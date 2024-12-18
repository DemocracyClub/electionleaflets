from django.core.management.base import BaseCommand
from django.db import connection
from leaflets.models import Leaflet

NAME_TO_GSS_RAW = """Aberavon	W07000049
Aberconwy	W07000058
Aberdeen North	S14000001
Aberdeen South	S14000002
Airdrie and Shotts	S14000003
Aldershot	E14000530
Aldridge-Brownhills	E14000531
Altrincham and Sale West	E14000532
Alyn and Deeside	W07000043
Amber Valley	E14000533
Angus	S14000004
Arfon	W07000057
Argyll and Bute	S14000005
Arundel and South Downs	E14000534
Ashfield	E14000535
Ashford	E14000536
Ashton-under-Lyne	E14000537
Aylesbury	E14000538
Ayr, Carrick and Cumnock	S14000006
Banbury	E14000539
Banff and Buchan	S14000007
Barking	E14000540
Barnsley Central	E14000541
Barnsley East	E14000542
Barrow and Furness	E14000543
Basildon and Billericay	E14000544
Basingstoke	E14000545
Bassetlaw	E14000546
Bath	E14000547
Batley and Spen	E14000548
Battersea	E14000549
Beaconsfield	E14000550
Beckenham	E14000551
Bedford	E14000552
Belfast East	N06000001
Belfast North	N06000002
Belfast South	N06000003
Belfast West	N06000004
Bermondsey and Old Southwark	E14000553
Berwickshire, Roxburgh and Selkirk	S14000008
Berwick-upon-Tweed	E14000554
Bethnal Green and Bow	E14000555
Beverley and Holderness	E14000556
Bexhill and Battle	E14000557
Bexleyheath and Crayford	E14000558
Birkenhead	E14000559
Birmingham, Edgbaston	E14000560
Birmingham, Erdington	E14000561
Birmingham, Hall Green	E14000562
Birmingham, Hodge Hill	E14000563
Birmingham, Ladywood	E14000564
Birmingham, Northfield	E14000565
Birmingham, Perry Barr	E14000566
Birmingham, Selly Oak	E14000567
Birmingham, Yardley	E14000568
Bishop Auckland	E14000569
Blackburn	E14000570
Blackley and Broughton	E14000571
Blackpool North and Cleveleys	E14000572
Blackpool South	E14000573
Blaenau Gwent	W07000072
Blaydon	E14000574
Blyth Valley	E14000575
Bognor Regis and Littlehampton	E14000576
Bolsover	E14000577
Bolton North East	E14000578
Bolton South East	E14000579
Bolton West	E14000580
Bootle	E14000581
Boston and Skegness	E14000582
Bosworth	E14000583
Bournemouth East	E14000584
Bournemouth West	E14000585
Bracknell	E14000586
Bradford East	E14000587
Bradford South	E14000588
Bradford West	E14000589
Braintree	E14000590
Brecon and Radnorshire	W07000068
Brent Central	E14000591
Brentford and Isleworth	E14000593
Brent North	E14000592
Brentwood and Ongar	E14000594
Bridgend	W07000073
Bridgwater and West Somerset	E14000595
Brigg and Goole	E14000596
Brighton, Kemptown	E14000597
Brighton, Pavilion	E14000598
Bristol East	E14000599
Bristol North West	E14000600
Bristol South	E14000601
Bristol West	E14000602
Broadland	E14000603
Bromley and Chislehurst	E14000604
Bromsgrove	E14000605
Broxbourne	E14000606
Broxtowe	E14000607
Buckingham	E14000608
Burnley	E14000609
Burton	E14000610
Bury North	E14000611
Bury South	E14000612
Bury St Edmunds	E14000613
Caerphilly	W07000076
Caithness, Sutherland and Easter Ross	S14000009
Calder Valley	E14000614
Camberwell and Peckham	E14000615
Camborne and Redruth	E14000616
Cambridge	E14000617
Cannock Chase	E14000618
Canterbury	E14000619
Cardiff Central	W07000050
Cardiff North	W07000051
Cardiff South and Penarth	W07000080
Cardiff West	W07000079
Carlisle	E14000620
Carmarthen East and Dinefwr	W07000067
Carmarthen West and South Pembrokeshire	W07000066
Carshalton and Wallington	E14000621
Castle Point	E14000622
Central Ayrshire	S14000010
Central Devon	E14000623
Central Suffolk and North Ipswich	E14000624
Ceredigion	W07000064
Charnwood	E14000625
Chatham and Aylesford	E14000626
Cheadle	E14000627
Chelmsford	E14000628
Chelsea and Fulham	E14000629
Cheltenham	E14000630
Chesham and Amersham	E14000631
Chesterfield	E14000632
Chichester	E14000633
Chingford and Woodford Green	E14000634
Chippenham	E14000635
Chipping Barnet	E14000636
Chorley	E14000637
Christchurch	E14000638
Cities of London and Westminster	E14000639
City of Chester	E14000640
City of Durham	E14000641
Clacton	E14000642
Cleethorpes	E14000643
Clwyd South	W07000062
Clwyd West	W07000059
Coatbridge, Chryston and Bellshill	S14000011
Colchester	E14000644
Colne Valley	E14000645
Congleton	E14000646
Copeland	E14000647
Corby	E14000648
Coventry North East	E14000649
Coventry North West	E14000650
Coventry South	E14000651
Crawley	E14000652
Crewe and Nantwich	E14000653
Croydon Central	E14000654
Croydon North	E14000655
Croydon South	E14000656
Cumbernauld, Kilsyth and Kirkintilloch East	S14000012
Cynon Valley	W07000070
Dagenham and Rainham	E14000657
Darlington	E14000658
Dartford	E14000659
Daventry	E14000660
Delyn	W07000042
Denton and Reddish	E14000661
Derby North	E14000662
Derbyshire Dales	E14000664
Derby South	E14000663
Devizes	E14000665
Dewsbury	E14000666
Doncaster Central	E14000668
Doncaster North	E14000669
Don Valley	E14000667
Dover	E14000670
Dudley North	E14000671
Dudley South	E14000672
Dulwich and West Norwood	E14000673
Dumfries and Galloway	S14000013
Dumfriesshire, Clydesdale and Tweeddale	S14000014
Dundee East	S14000015
Dundee West	S14000016
Dunfermline and West Fife	S14000017
Dwyfor Meirionnydd	W07000061
Ealing Central and Acton	E14000674
Ealing North	E14000675
Ealing, Southall	E14000676
Easington	E14000677
East Antrim	N06000005
Eastbourne	E14000684
East Devon	E14000678
East Dunbartonshire	S14000018
East Ham	E14000679
East Hampshire	E14000680
East Kilbride, Strathaven and Lesmahagow	S14000019
Eastleigh	E14000685
East Londonderry	N06000006
East Lothian	S14000020
East Renfrewshire	S14000021
East Surrey	E14000681
East Worthing and Shoreham	E14000682
East Yorkshire	E14000683
Eddisbury	E14000686
Edinburgh East	S14000022
Edinburgh North and Leith	S14000023
Edinburgh South	S14000024
Edinburgh South West	S14000025
Edinburgh West	S14000026
Edmonton	E14000687
Ellesmere Port and Neston	E14000688
Elmet and Rothwell	E14000689
Eltham	E14000690
Enfield North	E14000691
Enfield, Southgate	E14000692
Epping Forest	E14000693
Epsom and Ewell	E14000694
Erewash	E14000695
Erith and Thamesmead	E14000696
Esher and Walton	E14000697
Exeter	E14000698
Falkirk	S14000028
Fareham	E14000699
Faversham and Mid Kent	E14000700
Feltham and Heston	E14000701
Fermanagh and South Tyrone	N06000007
Filton and Bradley Stoke	E14000702
Finchley and Golders Green	E14000703
Folkestone and Hythe	E14000704
Forest of Dean	E14000705
Foyle	N06000008
Fylde	E14000706
Gainsborough	E14000707
Garston and Halewood	E14000708
Gateshead	E14000709
Gedling	E14000710
Gillingham and Rainham	E14000711
Glasgow Central	S14000029
Glasgow East	S14000030
Glasgow North	S14000031
Glasgow North East	S14000032
Glasgow North West	S14000033
Glasgow South	S14000034
Glasgow South West	S14000035
Glenrothes	S14000036
Gloucester	E14000712
Gordon	S14000037
Gosport	E14000713
Gower	W07000046
Grantham and Stamford	E14000714
Gravesham	E14000715
Great Grimsby	E14000716
Great Yarmouth	E14000717
Greenwich and Woolwich	E14000718
Guildford	E14000719
Hackney North and Stoke Newington	E14000720
Hackney South and Shoreditch	E14000721
Halesowen and Rowley Regis	E14000722
Halifax	E14000723
Haltemprice and Howden	E14000724
Halton	E14000725
Hammersmith	E14000726
Hampstead and Kilburn	E14000727
Harborough	E14000728
Harlow	E14000729
Harrogate and Knaresborough	E14000730
Harrow East	E14000731
Harrow West	E14000732
Hartlepool	E14000733
Harwich and North Essex	E14000734
Hastings and Rye	E14000735
Havant	E14000736
Hayes and Harlington	E14000737
Hazel Grove	E14000738
Hemel Hempstead	E14000739
Hemsworth	E14000740
Hendon	E14000741
Henley	E14000742
Hereford and South Herefordshire	E14000743
Hertford and Stortford	E14000744
Hertsmere	E14000745
Hexham	E14000746
Heywood and Middleton	E14000747
High Peak	E14000748
Hitchin and Harpenden	E14000749
Holborn and St Pancras	E14000750
Hornchurch and Upminster	E14000751
Hornsey and Wood Green	E14000752
Horsham	E14000753
Houghton and Sunderland South	E14000754
Hove	E14000755
Huddersfield	E14000756
Huntingdon	E14000757
Hyndburn	E14000758
Ilford North	E14000759
Ilford South	E14000760
Inverclyde	S14000038
Inverness, Nairn, Badenoch and Strathspey	S14000039
Ipswich	E14000761
Isle of Wight	E14000762
Islington North	E14000763
Islington South and Finsbury	E14000764
Islwyn	W07000077
Jarrow	E14000765
Keighley	E14000766
Kenilworth and Southam	E14000767
Kensington	E14000768
Kettering	E14000769
Kilmarnock and Loudoun	S14000040
Kingston and Surbiton	E14000770
Kingston upon Hull East	E14000771
Kingston upon Hull North	E14000772
Kingston upon Hull West and Hessle	E14000773
Kingswood	E14000774
Kirkcaldy and Cowdenbeath	S14000041
Knowsley	E14000775
Lagan Valley	N06000009
Lanark and Hamilton East	S14000042
Lancaster and Fleetwood	E14000776
Leeds Central	E14000777
Leeds East	E14000778
Leeds North East	E14000779
Leeds North West	E14000780
Leeds West	E14000781
Leicester East	E14000782
Leicester South	E14000783
Leicester West	E14000784
Leigh	E14000785
Lewes	E14000786
Lewisham, Deptford	E14000789
Lewisham East	E14000787
Lewisham West and Penge	E14000788
Leyton and Wanstead	E14000790
Lichfield	E14000791
Lincoln	E14000792
Linlithgow and East Falkirk	S14000043
Liverpool, Riverside	E14000793
Liverpool, Walton	E14000794
Liverpool, Wavertree	E14000795
Liverpool, West Derby	E14000796
Livingston	S14000044
Llanelli	W07000045
Loughborough	E14000797
Louth and Horncastle	E14000798
Ludlow	E14000799
Luton North	E14000800
Luton South	E14000801
Macclesfield	E14000802
Maidenhead	E14000803
Maidstone and The Weald	E14000804
Makerfield	E14000805
Maldon	E14000806
Manchester Central	E14000807
Manchester, Gorton	E14000808
Manchester, Withington	E14000809
Mansfield	E14000810
Meon Valley	E14000811
Meriden	E14000812
Merthyr Tydfil and Rhymney	W07000071
Mid Bedfordshire	E14000813
Mid Derbyshire	E14000814
Middlesbrough	E14000819
Middlesbrough South and East Cleveland	E14000820
Mid Dorset and North Poole	E14000815
Midlothian	S14000045
Mid Norfolk	E14000816
Mid Sussex	E14000817
Mid Ulster	N06000010
Mid Worcestershire	E14000818
Milton Keynes North	E14000821
Milton Keynes South	E14000822
Mitcham and Morden	E14000823
Mole Valley	E14000824
Monmouth	W07000054
Montgomeryshire	W07000063
Moray	S14000046
Morecambe and Lunesdale	E14000825
Morley and Outwood	E14000826
Motherwell and Wishaw	S14000047
Na h-Eileanan an Iar	S14000027
Neath	W07000069
Newark	E14000829
Newbury	E14000830
Newcastle-under-Lyme	E14000834
Newcastle upon Tyne Central	E14000831
Newcastle upon Tyne East	E14000832
Newcastle upon Tyne North	E14000833
New Forest East	E14000827
New Forest West	E14000828
Newport East	W07000055
Newport West	W07000056
Newry and Armagh	N06000011
Newton Abbot	E14000835
Normanton, Pontefract and Castleford	E14000836
Northampton North	E14000861
Northampton South	E14000862
North Antrim	N06000012
North Ayrshire and Arran	S14000048
North Cornwall	E14000837
North Devon	E14000838
North Dorset	E14000839
North Down	N06000013
North Durham	E14000840
North East Bedfordshire	E14000841
North East Cambridgeshire	E14000842
North East Derbyshire	E14000843
North East Fife	S14000049
North East Hampshire	E14000844
North East Hertfordshire	E14000845
North East Somerset	E14000846
North Herefordshire	E14000847
North Norfolk	E14000848
North Shropshire	E14000849
North Somerset	E14000850
North Swindon	E14000851
North Thanet	E14000852
North Tyneside	E14000853
North Warwickshire	E14000854
North West Cambridgeshire	E14000855
North West Durham	E14000856
North West Hampshire	E14000857
North West Leicestershire	E14000858
North West Norfolk	E14000859
North Wiltshire	E14000860
Norwich North	E14000863
Norwich South	E14000864
Nottingham East	E14000865
Nottingham North	E14000866
Nottingham South	E14000867
Nuneaton	E14000868
Ochil and South Perthshire	S14000050
Ogmore	W07000074
Old Bexley and Sidcup	E14000869
Oldham East and Saddleworth	E14000870
Oldham West and Royton	E14000871
Orkney and Shetland	S14000051
Orpington	E14000872
Oxford East	E14000873
Oxford West and Abingdon	E14000874
Paisley and Renfrewshire North	S14000052
Paisley and Renfrewshire South	S14000053
Pendle	E14000875
Penistone and Stocksbridge	E14000876
Penrith and The Border	E14000877
Perth and North Perthshire	S14000054
Peterborough	E14000878
Plymouth, Moor View	E14000879
Plymouth, Sutton and Devonport	E14000880
Pontypridd	W07000075
Poole	E14000881
Poplar and Limehouse	E14000882
Portsmouth North	E14000883
Portsmouth South	E14000884
Preseli Pembrokeshire	W07000065
Preston	E14000885
Pudsey	E14000886
Putney	E14000887
Rayleigh and Wickford	E14000888
Reading East	E14000889
Reading West	E14000890
Redcar	E14000891
Redditch	E14000892
Reigate	E14000893
Rhondda	W07000052
Ribble Valley	E14000894
Richmond Park	E14000896
Richmond (Yorks)	E14000895
Rochdale	E14000897
Rochester and Strood	E14000898
Rochford and Southend East	E14000899
Romford	E14000900
Romsey and Southampton North	E14000901
Rossendale and Darwen	E14000902
Ross, Skye and Lochaber	S14000055
Rotherham	E14000904
Rother Valley	E14000903
Rugby	E14000905
Ruislip, Northwood and Pinner	E14000906
Runnymede and Weybridge	E14000907
Rushcliffe	E14000908
Rutherglen and Hamilton West	S14000056
Rutland and Melton	E14000909
Saffron Walden	E14000910
Salford and Eccles	E14000911
Salisbury	E14000912
Scarborough and Whitby	E14000913
Scunthorpe	E14000914
Sedgefield	E14000915
Sefton Central	E14000916
Selby and Ainsty	E14000917
Sevenoaks	E14000918
Sheffield, Brightside and Hillsborough	E14000921
Sheffield Central	E14000919
Sheffield, Hallam	E14000922
Sheffield, Heeley	E14000923
Sheffield South East	E14000920
Sherwood	E14000924
Shipley	E14000925
Shrewsbury and Atcham	E14000926
Sittingbourne and Sheppey	E14000927
Skipton and Ripon	E14000928
Sleaford and North Hykeham	E14000929
Slough	E14000930
Solihull	E14000931
Somerton and Frome	E14000932
Southampton, Itchen	E14000955
Southampton, Test	E14000956
South Antrim	N06000014
South Basildon and East Thurrock	E14000933
South Cambridgeshire	E14000934
South Derbyshire	E14000935
South Dorset	E14000936
South Down	N06000015
South East Cambridgeshire	E14000937
South East Cornwall	E14000938
Southend West	E14000957
South Holland and The Deepings	E14000939
South Leicestershire	E14000940
South Norfolk	E14000941
South Northamptonshire	E14000942
Southport	E14000958
South Ribble	E14000943
South Shields	E14000944
South Staffordshire	E14000945
South Suffolk	E14000946
South Swindon	E14000947
South Thanet	E14000948
South West Bedfordshire	E14000949
South West Devon	E14000950
South West Hertfordshire	E14000951
South West Norfolk	E14000952
South West Surrey	E14000953
South West Wiltshire	E14000954
Spelthorne	E14000959
Stafford	E14000965
Staffordshire Moorlands	E14000966
St Albans	E14000960
Stalybridge and Hyde	E14000967
St Austell and Newquay	E14000961
Stevenage	E14000968
St Helens North	E14000962
St Helens South and Whiston	E14000963
Stirling	S14000057
St Ives	E14000964
Stockport	E14000969
Stockton North	E14000970
Stockton South	E14000971
Stoke-on-Trent Central	E14000972
Stoke-on-Trent North	E14000973
Stoke-on-Trent South	E14000974
Stone	E14000975
Stourbridge	E14000976
Strangford	N06000016
Stratford-on-Avon	E14000977
Streatham	E14000978
Stretford and Urmston	E14000979
Stroud	E14000980
Suffolk Coastal	E14000981
Sunderland Central	E14000982
Surrey Heath	E14000983
Sutton and Cheam	E14000984
Sutton Coldfield	E14000985
Swansea East	W07000048
Swansea West	W07000047
Tamworth	E14000986
Tatton	E14000987
Taunton Deane	E14000988
Telford	E14000989
Tewkesbury	E14000990
The Cotswolds	E14000991
The Wrekin	E14000992
Thirsk and Malton	E14000993
Thornbury and Yate	E14000994
Thurrock	E14000995
Tiverton and Honiton	E14000996
Tonbridge and Malling	E14000997
Tooting	E14000998
Torbay	E14000999
Torfaen	W07000053
Torridge and West Devon	E14001000
Totnes	E14001001
Tottenham	E14001002
Truro and Falmouth	E14001003
Tunbridge Wells	E14001004
Twickenham	E14001005
Tynemouth	E14001006
Upper Bann	N06000017
Uxbridge and South Ruislip	E14001007
Vale of Clwyd	W07000060
Vale of Glamorgan	W07000078
Vauxhall	E14001008
Wakefield	E14001009
Wallasey	E14001010
Walsall North	E14001011
Walsall South	E14001012
Walthamstow	E14001013
Wansbeck	E14001014
Wantage	E14001015
Warley	E14001016
Warrington North	E14001017
Warrington South	E14001018
Warwick and Leamington	E14001019
Washington and Sunderland West	E14001020
Watford	E14001021
Waveney	E14001022
Wealden	E14001023
Weaver Vale	E14001024
Wellingborough	E14001025
Wells	E14001026
Welwyn Hatfield	E14001027
Wentworth and Dearne	E14001028
West Aberdeenshire and Kincardine	S14000058
West Bromwich East	E14001029
West Bromwich West	E14001030
West Dorset	E14001031
West Dunbartonshire	S14000059
West Ham	E14001032
West Lancashire	E14001033
Westminster North	E14001036
Westmorland and Lonsdale	E14001037
Weston-Super-Mare	E14001038
West Suffolk	E14001034
West Tyrone	N06000018
West Worcestershire	E14001035
Wigan	E14001039
Wimbledon	E14001040
Winchester	E14001041
Windsor	E14001042
Wirral South	E14001043
Wirral West	E14001044
Witham	E14001045
Witney	E14001046
Woking	E14001047
Wokingham	E14001048
Wolverhampton North East	E14001049
Wolverhampton South East	E14001050
Wolverhampton South West	E14001051
Worcester	E14001052
Workington	E14001053
Worsley and Eccles South	E14001054
Worthing West	E14001055
Wrexham	W07000044
Wycombe	E14001056
Wyre and Preston North	E14001057
Wyre Forest	E14001058
Wythenshawe and Sale East	E14001059
Yeovil	E14001060
Ynys Môn	W07000041
York Central	E14001061
York Outer	E14001062
"""


NAME_TO_GSS = dict(line.split("\t") for line in NAME_TO_GSS_RAW.splitlines())

EPOCH = "2015-03-03"


class NoPostcodesMatchException(ValueError): ...


class Command(BaseCommand):
    help = (
        "Map postcodes from a model to NUTS1 regions using a CSV mapping file."
    )

    def lookup_postcode_and_const(self, leaflet):
        self.cursor.execute(
            f"""
                        SELECT pcds
                        FROM "ONSPD_NOV_2016_UK"
                        WHERE replace(pcd, ' ', '') ~ '^.{leaflet.postcode.replace(' ', '')}$'
                        AND pcon='{NAME_TO_GSS[leaflet.constituency.name]}'
                        ;""",
        )
        row = self.cursor.fetchall()
        if not row:
            raise NoPostcodesMatchException()

        return row[0][0]

    def lookup_postcode_only(self, leaflet):
        self.cursor.execute(
            f"""
            SELECT pcds
            FROM "ONSPD_NOV_2016_UK"
            WHERE replace(pcd, ' ', '') ~ '^.{leaflet.postcode.replace(' ', '')}$';
            """,
        )
        row = self.cursor.fetchall()
        if not row:
            print(f"{leaflet.postcode} NOT FOUND")
            return None
        if len(row) > 1:
            print(
                f"{len(row)}\t{leaflet.postcode}\t{leaflet.constituency.name}\t{NAME_TO_GSS[leaflet.constituency.name]}"
            )
            return None

        return row[0][0]

    def handle(self, *args, **options):
        self.cursor = connection.cursor()
        EPOCH = "2015-03-03"

        self.out_map = {}

        qs = (
            Leaflet.objects.filter(date_uploaded__lte=EPOCH)
            .select_related("constituency")
            .order_by("postcode")
            .distinct("postcode")
        )
        for leaflet in qs:
            if not leaflet.constituency:
                continue

            try:
                new_postcode = self.lookup_postcode_and_const(leaflet)
            except NoPostcodesMatchException:
                new_postcode = self.lookup_postcode_only(leaflet)
            self.out_map[leaflet.postcode] = new_postcode

        # For writing to disk
        with open("fixed_postcodes.tsv", "w") as f:
            for k, v in self.out_map.items():
                if v:
                    f.write(f"{k}\t{v}\n")

        self.write_to_db()

    def write_to_db(self):
        # Manual fixes
        with open("fixed_postcodes.tsv", "r") as f:
            out_map = dict(line.split("\t") for line in f.readlines())

        out_map["G1- 1PB"] = "SG1 1PB"
        out_map["Y5 3FH."] = "DY5 3FH"

        for old_postcode, new_postcode in out_map.items():
            new_postcode = new_postcode.strip()
            print(f"Setting {old_postcode} to {new_postcode}")
            # Uncomment for actual use
            Leaflet.objects.filter(date_uploaded__lte=EPOCH).filter(
                postcode=old_postcode
            ).update(postcode=new_postcode)
