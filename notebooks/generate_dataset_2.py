mission = Mission.objects.create(name="Monitoring 13",
                                 description="",
                                 keywords="")

Strategy.register_values()
FeedbackField.register_values()
FeedbackScoreField.register_values()


strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")


task0_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 0. Czy dotyczy", order=0)
task1_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 1", order=1)
task1_2 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 2", order=2)
task1_3_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 3.1", order=3)
task1_3_2 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 3.2", order=4)
task1_4 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 4", order=5)
task1_5_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 5.1", order=6)
task1_5_2 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 5.2", order=7)
task1_6 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 6", order=8)
task1_7 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 1. Facebook - 7", order=9)
task2_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 1", order=10)
task2_2 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 2", order=11)
task2_3_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 3.1", order=12)
task2_3_2 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 3.2", order=13)
task2_4 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 4", order=14)
task2_5_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 5.1", order=15)
task2_5_2 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 5.2", order=16)
task2_6 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 6", order=17)
task2_7 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 2. Twitter - 7", order=18)
task3_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 3. Forum - 1", order=19)
task4_1 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 3. Oficjalny profil - 1", order=20)
task4_2 = Task.objects.create(mission=mission, strategy=strategy, name="Monitoring 13 - 4. Oficjalny profil - 2", order=21)


# Task templates
template1 = ItemTemplate.objects.create(name="Monitoring 11 - pytanie jednokrotnego wyboru")
template2 = ItemTemplate.objects.create(name="Monitoring 12 - pytanie wielokrotnego wyboru")

## Task items


urls = ['18249_25044.pdf', '18052_24893.pdf', '18336_25134.pdf', '18250_25045.pdf', '18289_25076.pdf', '18334_25133.pdf', '18058_24897.pdf', '18260_25048.pdf', '18558_25463.pdf', '18036_24883.pdf', '18311_25114.pdf', '18274_25061.pdf', '18050_24892.pdf', '18285_25072.pdf', '17852_24547.pdf', '17984_24838.pdf', '18330_25130.pdf', '18431_25358.pdf', '18009_24863.pdf', '18234_25030.pdf', '17798_24498.pdf', '18235_25031.pdf', '18300_25107.pdf', '17963_24819.pdf', '17884_24573.pdf', '17911_24598.pdf', '18086_24923.pdf', '18204_25004.pdf', '17952_24728.pdf', '18208_25008.pdf', '18354_25266.pdf', '17791_24485.pdf', '17996_24851.pdf', '18207_25007.pdf', '17947_24715.pdf', '18245_25038.pdf', '18279_25066.pdf', '17876_24568.pdf', '18320_25124.pdf', '18244_25037.pdf', '18322_25126.pdf', '17825_24521.pdf', '18310_25113.pdf', '18119_24940.pdf', '18326_25128.pdf', '18038_24885.pdf', '18269_25055.pdf', '18077_24914.pdf', '18056_24895.pdf', '18201_25001.pdf', '18205_25005.pdf', '18141_24957.pdf', '18215_25024.pdf', '18280_25067.pdf', '18297_25083.pdf', '18007_24860.pdf', '18246_25041.pdf', '17997_24852.pdf', '18241_25036.pdf', '18308_25111.pdf', '18318_25121.pdf', '18189_24994.pdf', '17950_24721.pdf', '18020_24873.pdf', '18288_25075.pdf', '18580_25502.pdf', '18039_24886.pdf', '18140_24954.pdf', '18169_24977.pdf', '18296_25082.pdf', '18162_24974.pdf', '18396_25317.pdf', '18273_25060.pdf', '18074_24907.pdf', '17968_24822.pdf', '18107_24934.pdf', '18213_25022.pdf', '17990_24841.pdf', '18332_25131.pdf', '17801_24503.pdf', '17962_24817.pdf', '18333_25132.pdf', '18266_25052.pdf', '17830_24527.pdf', '18085_24922.pdf', '18307_25110.pdf', '17828_24525.pdf', '18475_25398.pdf', '17806_24505.pdf', '18200_25000.pdf', '18317_25120.pdf', '18144_24960.pdf', '18048_24891.pdf', '18131_24948.pdf', '18272_25058.pdf', '18415_25336.pdf', '17998_24855.pdf', '18263_25049.pdf', '18209_25010.pdf', '17900_24585.pdf', '18175_24981.pdf', '18247_25041.pdf', '18106_24933.pdf', '18145_24961.pdf', '17856_24552.pdf', '17826_24523.pdf', '18268_25053.pdf', '18108_24935.pdf', '18117_24938.pdf', '18079_24918.pdf', '17861_24554.pdf', '18172_24980.pdf', '18081_24920.pdf', '18057_24896.pdf', '18147_24964.pdf', '17892_24580.pdf', '18001_24857.pdf', '18146_24962.pdf', '18064_24901.pdf', '17805_24505.pdf', '18275_25062.pdf', '18340_25138.pdf', '18316_25119.pdf', '17866_24560.pdf', '18191_24996.pdf', '18298_25085.pdf', '18171_24978.pdf', '18295_25081.pdf', '18178_24984.pdf', '18290_25077.pdf', '18276_25064.pdf', '18217_25026.pdf', '17992_24845.pdf', '18091_24927.pdf', '18476_25399.pdf']

mp = MissionPackages.objects.create(mission=mission, strategy=strategy)





strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")

urls = ['18249_25044.pdf', '18052_24893.pdf', '18336_25134.pdf', '18250_25045.pdf', '18289_25076.pdf', '18334_25133.pdf', '18058_24897.pdf', '18260_25048.pdf', '18558_25463.pdf', '18036_24883.pdf', '18311_25114.pdf', '18274_25061.pdf', '18050_24892.pdf', '18285_25072.pdf', '17852_24547.pdf', '17984_24838.pdf', '18330_25130.pdf', '18431_25358.pdf', '18009_24863.pdf', '18234_25030.pdf', '17798_24498.pdf', '18235_25031.pdf', '18300_25107.pdf', '17963_24819.pdf', '17884_24573.pdf', '17911_24598.pdf', '18086_24923.pdf', '18204_25004.pdf', '17952_24728.pdf', '18208_25008.pdf', '18354_25266.pdf', '17791_24485.pdf', '17996_24851.pdf', '18207_25007.pdf', '17947_24715.pdf', '18245_25038.pdf', '18279_25066.pdf', '17876_24568.pdf', '18320_25124.pdf', '18244_25037.pdf', '18322_25126.pdf', '17825_24521.pdf', '18310_25113.pdf', '18119_24940.pdf', '18326_25128.pdf', '18038_24885.pdf', '18269_25055.pdf', '18077_24914.pdf', '18056_24895.pdf', '18201_25001.pdf', '18205_25005.pdf', '18141_24957.pdf', '18215_25024.pdf', '18280_25067.pdf', '18297_25083.pdf', '18007_24860.pdf', '18246_25041.pdf', '17997_24852.pdf', '18241_25036.pdf', '18308_25111.pdf', '18318_25121.pdf', '18189_24994.pdf', '17950_24721.pdf', '18020_24873.pdf', '18288_25075.pdf', '18580_25502.pdf', '18039_24886.pdf', '18140_24954.pdf', '18169_24977.pdf', '18296_25082.pdf', '18162_24974.pdf', '18396_25317.pdf', '18273_25060.pdf', '18074_24907.pdf', '17968_24822.pdf', '18107_24934.pdf', '18213_25022.pdf', '17990_24841.pdf', '18332_25131.pdf', '17801_24503.pdf', '17962_24817.pdf', '18333_25132.pdf', '18266_25052.pdf', '17830_24527.pdf', '18085_24922.pdf', '18307_25110.pdf', '17828_24525.pdf', '18475_25398.pdf', '17806_24505.pdf', '18200_25000.pdf', '18317_25120.pdf', '18144_24960.pdf', '18048_24891.pdf', '18131_24948.pdf', '18272_25058.pdf', '18415_25336.pdf', '17998_24855.pdf', '18263_25049.pdf', '18209_25010.pdf', '17900_24585.pdf', '18175_24981.pdf', '18247_25041.pdf', '18106_24933.pdf', '18145_24961.pdf', '17856_24552.pdf', '17826_24523.pdf', '18268_25053.pdf', '18108_24935.pdf', '18117_24938.pdf', '18079_24918.pdf', '17861_24554.pdf', '18172_24980.pdf', '18081_24920.pdf', '18057_24896.pdf', '18147_24964.pdf', '17892_24580.pdf', '18001_24857.pdf', '18146_24962.pdf', '18064_24901.pdf', '17805_24505.pdf', '18275_25062.pdf', '18340_25138.pdf', '18316_25119.pdf', '17866_24560.pdf', '18191_24996.pdf', '18298_25085.pdf', '18171_24978.pdf', '18295_25081.pdf', '18178_24984.pdf', '18290_25077.pdf', '18276_25064.pdf', '18217_25026.pdf', '17992_24845.pdf', '18091_24927.pdf', '18476_25399.pdf']

names = set(Package.objects.values_list("name", flat=True))

mission = Mission.objects.get(id=1)


template = ItemTemplate.objects.get(name="Misja 1 - szablon")
template2 = ItemTemplate.objects.get(name="Misja 1 - szablon2")



task1 = Task.objects.get(mission=mission, name="Pytanie 1 - drugie")
task2 = Task.objects.get(mission=mission, name="Pytanie 1.1 - drugie")
task3 = Task.objects.get(mission=mission, name="Pytanie 1.2 - drugie")
task4 = Task.objects.get(mission=mission, name="Pytanie 2 - drugie")
task5 = Task.objects.get(mission=mission, name="Pytanie 3.1 - drugie")
task6 = Task.objects.get(mission=mission, name="Pytanie 3.2 - drugie")
task7 = Task.objects.get(mission=mission, name="Pytanie 3.3 - drugie")
task8 = Task.objects.get(mission=mission, name="Pytanie 4 - drugie")




mp = MissionPackages.objects.filter(mission=mission).first()


for order, url in enumerate(urls[30:50]):
    if url.split('.')[0] in names: 
        continue 

    package = Package.objects.create(parent=mp, order=mp.packages.count(), name=url.split('.')[0])
    url = "http://62.181.9.75:8890/static/pdf/" + url

    ## Task 1
    data = {
        "pdf_source": url,
        "question": "Czy Starostwo Powiatowe posiada wdrożony elektroniczny obieg dokumentów?",
        "field_answers": ["Tak", "Nie", "Trudno powiedzieć", "Brak informacji"],
    }
    item = Item.objects.create(task=task1, template=template1, order=1, data=data)
    item.package = package
    item.save()


    ## Task 1.1
    data = {
        "pdf_source": url,
        "question": "Czy jest to główna forma dekretacji dokumentów, czy tylko wspomagająca?",
        "field_answers": ["Główna", "Wspomagająca", "Trudno powiedzieć", "Brak informacji"],
    }
    item = Item.objects.create(task=task2, template=template1, order=2, data=data)
    item.package = package
    item.save()

    ## Task 1.1
    data = {
        "pdf_source": url,
        "question": "Czy elektroniczny obieg dokumentów starostwa jest kompatybilny z platformą EPUAP?",
        "field_answers": ["Tak", "Nie", "Trudno powiedzieć", "Brak informacji"],
    }
    item = Item.objects.create(task=task3, template=template1, order=3, data=data)
    item.package = package
    item.save()

    ## Task 2
    data = {
        "pdf_source": url,
        "question": "Czy wszystkie decyzje administracyjne w sprawach, których dotyczy art. 39 KPA, są doręczane w sposób wskazany w tym artykule: https://www.gov.pl/cyfryzacja/koniec-wymiany-papierow-miedzy-urzedami ?", 
        "field_answers": ["Tak", "Nie", "Trudno powiedzieć", "Brak informacji"],
    }
    item = Item.objects.create(task=task4, template=template1, order=4, data=data)
    item.package = package
    item.save()

    ## Task 3.1
    data = {
        "pdf_source": url,
        "question": "Czy dokument zawiera odpowiedź na to pytanie: \"Jeżeli nie wszystkie ww. decyzje są przekazywane podmiotom publicznym za pomocą platformy uPUAP, to jakie względy organizacyjne/techniczne/inne stoja na przeszkodzie?\"", 
        "field_answers": ["Tak", "Nie", "Trudno powiedzieć"],
    }
    item = Item.objects.create(task=task5, template=template1, order=5, data=data)
    item.package = package
    item.save()

    ## Task 3.2
    data = {
        "pdf_source": url,
        "question": "Jeśli nie wszystkie ww. decyzje są przekazywane podmiotom publicznym za pomocą platformy ePUAP, to jakie względy organizacyjne/ techniczne/ inne stoją na przeszkodzie?", 
        "field_answers": [
            "Odbiorca chce otrzymać odpowiedź tradycyjną pocztą",
            "Urząd odpowiada w takiej formie, w jakiej otrzymał pismo",
            "Odbiorca nie posiada Elektronicznej Skrzynki Podawczej na platformie EPUAP",
            "Konieczność posiadania przez odbiorcę oryginału dokumentu (np. projekty budowlane)",
            "Żadne z powyższych"
        ],
    }
    item = Item.objects.create(task=task6, template=template2, order=6, data=data)
    item.package = package
    item.save()

    ## Task 3.3
    data = {
        "pdf_source": url,
        "question": "Jeśli nie wszystkie ww. decyzje są przekazywane podmiotom publicznym za pomocą platformy ePUAP, to jakie względy organizacyjne/ techniczne/ inne stoją na przeszkodzie?", 
        "field_answers": [
            "Niewielu urzędników posiada podpis elektroniczny – jest drogi",
            "Korzystanie z EPUAP-u zwiększa koszty i wydłuża czas (czasochłonne skanowanie)",
            "Zbyt obszerne załączniki (z dużą ilością stron), które nie przechodzą przez EPUAP",
            "Urząd nie ma systemu Elektronicznego Obiegu Dokumentów",
            "System Elektronicznego Obiegu Dokumentów (EOD, wymiennie używany skrót EZD) nie jest kompatybilny z EPUAP-em",
            "Problemy techniczne - awaryjność platformy EPUAP",
            "Żadne z powyższych"
        ]
    }
    item = Item.objects.create(task=task7, template=template2, order=7, data=data)
    item.package = package
    item.save()

    ## Task 4
    data = {
        "pdf_source": url,

        "question": "Czy starostwo kontaktowało się z Ministerstwem Cyfryzacji w celu usunięcia ww. przeszkód?", 
        "field_answers": ["Tak", "Nie", "Trudno powiedzieć", "Brak informacji"],
    }
    item = Item.objects.create(task=task8, template=template1, order=8, data=data)
    item.package = package
    item.save()


