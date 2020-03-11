import re

# print(re.findall(r'paper/\d+/reference','paper/1559136758/reference'))

# temp = ' CITATIONS* (1,318)'
#
# '''
#          CITATIONS* (567)
#          CITATIONS* (1,318)
#          CITATIONS* (460)
#          CITATIONS* (481)
#          CITATIONS* (603)
#          CITATIONS* (136)
#          '''
# Citation_Count= re.findall('\(.+\)', temp)[0][1:-1]
# print(Citation_Count)

# base_url = r'https://academic.microsoft.com/search?q=blockchain&f=&orderBy=0&skip={}&take=10'
#
# with open('urls.txt', 'w', encoding='utf-8') as f:
#     for i in range(0, 4990 + 1):
#         f.write(base_url.format(i * 10)+"\n")
#         print(i)


text = {
    "url": "https://academic.microsoft.com/paper/1559136758/reference",
    "Pub_Title": "Decentralizing Privacy: Using Blockchain to Protect Personal Data",
    "Year": "2015",
    "Pub_Outlet": "IEEE Symposium on Security and Privacy",
    "Citation_Count": "567",
    "Abstract": "The recent increase in reported incidents of surveillance and security breaches compromising users' privacy call into question the current model, in which third-parties collect and control massive amounts of personal data. Bit coin has demonstrated in the financial space that trusted, auditable computing is possible using a decentralized network of peers accompanied by a public ledger. In this paper, we describe a decentralized personal data management system that ensures users own and control their data. We implement a protocol that turns a block chain into an automated access-control manager that does not require trust in a third party. Unlike Bit coin, transactions in our system are not strictly financial -- they are used to carry instructions, such as storing, querying and sharing data. Finally, we discuss possible future extensions to block chains that could harness them into a well-rounded solution for trusted computing problems in society.",
    "Author": [
        [
            "Guy Zyskind",
            "Massachusetts Institute of Technology"
        ],
        [
            "Oz Nathan",
            "Tel Aviv University"
        ],
        [
            "Alex 'Sandy' Pentland",
            "Massachusetts Institute of Technology"
        ]
    ],
    "Tag": [
        "Trusted Computing",
        "Privacy software",
        "Privacy by Design",
        "Ledger",
        "Internet privacy",
        "Information privacy",
        "Data management",
        "Computer security",
        "Computer science",
        "Blockchain"
    ]
}

print(len(text['Author']))

# if len(text['Author']) < 12:

try:
    Author1 = text['Author'][0][0]
    Author1_Insttute = text['Author'][0][1]
    Author2 = text['Author'][1][0]
    Author2_Insttute = text['Author'][1][1]
    Author3 = text['Author'][2][0]
    Author3_Insttute = text['Author'][2][1]
    Author4 = text['Author'][3][0]
    Author4_Insttute = text['Author'][3][1]
    Author5 = text['Author'][4][0]
    Author5_Insttute = text['Author'][4][1]
    Author6 = text['Author'][5][0]
    Author6_Insttute = text['Author'][5][1]
    Author7 = text['Author'][6][0]
    Author7_Insttute = text['Author'][6][1]

    Author8 = text['Author'][7][0]
    Author8_Insttute = text['Author'][7][1]
    Author9 = text['Author'][8][0]
    Author9_Insttute = text['Author'][8][1]
    Author10 = text['Author'][9][0]
    Author10_Insttute = text['Author'][9][1]
    Author11 = text['Author'][10][0]
    Author11_Insttute = text['Author'][10][1]
    Author12 = text['Author'][11][0]
    Author12_Insttute = text['Author'][11][1]
except Exception as e:
    print(e)
