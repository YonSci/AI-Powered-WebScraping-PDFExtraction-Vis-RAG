# config.py

CATEGORIES_LIST = [
    "Building", "CPI", "Customer Price Index", "Construction", "Surveys",
    "GDP", "Constant Prices", "Gross Domestic Product", "Demographics",
    "Social", "Crime", "Culture", "Education", "Gender", "Household Surveys",
    "Poverty", "Labor", "Population", "Censuses", "Public Health", "Fishing",
    "Environment", "Climate", "Land", "Water Supply", "Macro Economic",
    "Banking and Currency", "Government Finance", "Insurance", "Indices",
    "External Trade", "Indicators", "National Standard Indicators",
    "Human Assets", "Economic Vulnerability", "Finance", "Exports", "Imports",
    "Merchandise", "Interest Rates", "Production", "Agriculture", "Energy",
    "Migration", "Tourism", "Communication", "Transport", "Business",
    "Industry", "Mining", "Income", "Expenditure", "National Accounts", "Bulletin",
]


COUNTRY_URLS = {
    "Algeria": [
        "http://www.ons.dz/"
    ],
    "Angola": [
        "http://www.ine.gov.ao/xportal/xmain?xpid=ine"
    ],
    "Benin": [
        "https://instad.bj/"
    ],
    "Botswana": [
        "https://www.statsbots.org.bw/",
    ],
    "Burkina Faso": [
        "http://www.insd.bf/"
    ],
    "Burundi": [
        "http://www.isteebu.bi/index.php/publications/indices-des-prix/ipc"
    ],
    "Cameroon": [
        "https://ins-cameroun.cm/"
    ],
    "Cape Verde": [
        "http://www.bcv.cv/vPT/Publicacoes%20e%20Intervencoes/indicadoreseconomicosefinanceiros/Paginas/IndicadoresEcon%C3%B3micoseFinanceirosOutubrode2010.aspx?lst=1"
    ],
    "Central African Republic": [
        "http://www.ins.cf/"
    ],
    "Comoros": [
        "http://www.ins.ci/n/"
    ],
    "Congo": [
        "http://www.bcc.cd/index.php?option=com_content&view=category&id=73&Itemid=14",
        "http://www.bcc.cd/index.php?option=com_content&view=category&id=73&Itemid=14"
    ],
    "Côte d'Ivoire": [
        "http://www.ins.ci/n/"
    ],
    "Democratic Republic of the Congo": [
        "http://www.bcc.cd/index.php?option=com_content&view=category&id=73&Itemid=14"
    ],
    "Djibouti": [
        "http://www.insd.dj/ipc.php"
    ],
    "Egypt": [
        "https://www.cbe.org.eg/en/news-publications",
    ],
    "Eritrea": [
        ""
    ],
    "Ethiopia": [
        "http://www.csa.gov.et/"
    ],
    "Gabon": [
        "http://www.stat-gabon.org/"
    ],
    "Gambia": [
        "https://www.gbosdata.org/"
    ],
    "Ghana": [
        "http://www.statsghana.gov.gh/"
    ],
    "Guinea": [
        "http://www.stat-guinee.org/index.php/publications-ins/publications-infra-annuelles/ihpc"
    ],
    "Guinea-Bissau": [
        "http://www.stat-guinebissau.com/publicacao/publicacao.htm"
    ],
    "Equatorial Guinea": [
        "http://www.inege.gq/"
    ],
    "Kenya": [
        "http://www.knbs.or.ke/",
        "https://www.knbs.or.ke/all-reports/"
    ],
    "Lesotho": [
        "http://www.bos.gov.ls/"
    ],
    "Liberia": [
        "https://cbl.org.lr/2content.php?sub=222&related=29&third=222&pg=sp&pt=Monthly Economic Review"
    ],
    "Libyan": [
        "http://bsc.ly/?P=2&n_Id=58#"
    ],
    "Madagascar": [
        "http://www.instat.mg/enquete-innovante/contexte/"
    ],
    "Malawi": [
        "https://www.nsomalawi.mw/publications/economy/consumer-price-indices-september-2024",
        "http://www.nsomalawi.mw/",
        "https://www.nsomalawi.mw/publications/economy/",
    ],
    "Mali": [
        "http://www.instat-mali.org/index.php/publications/2014-10-23-11-37-06/indice-harmonise-des-prix-a-la-consommation"
    ],
    "Mauritania": [
        "http://www.ons.mr/"
    ],
    "Mauritius": [
        "http://statsmauritius.govmu.org/English/Publications/Pages/Archive/Arch-Mthly-CPI.aspx"
    ],
    "Morocco": [
        "http://www.hcp.ma/IPC_r15.html"
    ],
    "Mozambique": [
        "http://www.ine.gov.mz/estatisticas/estatisticas-economicas/indice-de-preco-no-consumidor/notas-de-imprensa/mocambique"
    ],
    "Namibia": [
        "http://nsa.org.na/page/publications/"
    ],
    "Niger": [
        "http://www.stat-niger.org/statistique/index.php/publication/publications-de-l-ins/indice/item/231"
    ],
    "Nigeria": [
        "http://www.nigerianstat.gov.ng/"
    ],
    "Rwanda": [
        "https://www.statistics.gov.rw/statistical-publications/subject/price-indices-%28cpi%2C-ppi%2C-iip%29",
    ],
    "Sao Tome and Principe": [
        "https://www.ine.st/"
    ],
    "Senegal": [
        "http://www.ansd.sn/index.php?option=com_ansd&view=titrepublication&id=16"
    ],
    "Seychelles": [
        "http://www.nbs.gov.sc/downloads/economic-statistics/consumer-price-index/2017"
    ],
    "Sierra Leone": [
        "https://www.statistics.sl/cpi/"
    ],
    "Somalia": [
        ""
    ],
    "South Africa": [
        "http://www.statssa.gov.za/?page_id=1866&PPN=P0141"
    ],
    "South Sudan": [
        "http://www.ssnbss.org/home/documents/surveys/consumer-price-index"
    ],
    "Sudan": [
        "http://cbs.gov.sd/"
    ],
    "Eswatini": [
        "https://swazistat.wordpress.com/category/economic-statistics/price-statistics/"
    ],
    "TChad": [
        "https://www.inseed.td/"
    ],
    "Togo": [
        "http://www.stat-togo.org/index.php/ihpc"
    ],
    "Tunisia": [
        "http://www.ins.tn/"
    ],
    "Uganda": [
        "https://www.ubos.org/explore-statistics/0/"
    ],
    "United Republic of Tanzania": [
        "http://www.nbs.go.tz/"
    ],
    "Zambia": [
        "https://www.zamstats.gov.zm/index.php/publications/category/53-2017"
    ],
    "Zimbabwe": [
        "http://www.zimstat.co.zw/prices-statistics-zimbabwe"
    ]
}

