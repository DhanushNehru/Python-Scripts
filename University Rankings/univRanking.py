import pandas as pd

def getInformation(selectedCountry, rankingFileName, capitalsFileName):
    # add selected country
    # Total number of universities
    # show countries
    # show continents
    # calculate average score (sum of all uni scores within the selected country) / (number of universities within the selected country)
    # display the average score
    # calculate the relative score (average score) / (The highest score within the continent where the university is selected)

    available_countries = 0
    counter = 0
    countries = ""
    continents = ""
    countries_lst = []
    continents_lst = []
    TopUni = pd.read_csv(rankingFileName)
    Capitals = pd.read_csv(capitalsFileName)
    country_counter = 0
    country_counter_rank = 1

    file = open("output.txt", "w")  # open output.txt file where output is stored

    for line in range(len(TopUni)):
        counter += 1

    file.write("Total number of Universities => {}\n" .format(counter))  # PART 1 TOTAL NUMBER OF UNIVERSITIES

    # LISTING ALL AVAILABLE COUNTRIES WITHIN THE FILE
    for country in Capitals["Country Name"]:
        if country not in countries_lst:
            countries_lst.append(country)
        available_countries += 1

    for country in countries_lst:
        if countries == "":
            countries = countries + country
        else:
            countries = countries + ", " + country

    file.write("Available countries => {}\n" .format(countries))  # PART 2 AVAILABLE COUNTRIES

    # FINDING ALL AVAILABLE CONTINENTS WITHIN THE FILE
    for continent in Capitals["Continent"]:
        if continent not in continents_lst:
            continents_lst.append(continent)

    for continent in continents_lst:
        if continents == "":
            continents = continents + continent
        else:
            continents = continents + ", " + continent

    file.write("Available Continents => {}\n" .format(continents))  # PART 3 AVAILABLE CONTINENTS

    # FINDING THE INTERNATIONAL RANK OF COUNTRIES ASSOCIATED WITH THE SELECTED COUNTRY
    for country in TopUni["Country"]:
        if country == selectedCountry:
            file.write("At international rank => {} the university name is => {}\n" .format(country_counter_rank, TopUni["Institution name"][country_counter]))  # PART 4 INTERNATIONAL RANK
        country_counter += 1
        country_counter_rank += 1

    country_counter = 0
    country_national_counter_rank = 1

    for country in TopUni["Country"]:
        if country == selectedCountry:
            file.write("At national rank => {} the university name is => {}\n" .format(country_national_counter_rank, TopUni["Institution name"][country_counter]))  # PART 5 NATIONAL RANK
            country_national_counter_rank += 1
        country_counter += 1

    number_of_universities = 0
    university_score = 0
    TopUni = pd.read_csv(rankingFileName)
    counter = 0

    for country in TopUni["Country"]:
        if selectedCountry == country:
            university_score += TopUni["Score"][counter]
            number_of_universities += 1
        counter += 1

    # THE AVERAGE SCORE CALCULATIONS
    averageScore = university_score / number_of_universities
    file.write("The average score => {}%\n" .format(round(averageScore, 1)))  # PART 6 AVERAGE SCORE                                                                                                         # PART 6

    number_of_universities = 0
    university_score = 0
    TopUni = pd.read_csv(rankingFileName)
    Capitals = pd.read_csv(capitalsFileName)
    highestScore1 = 0
    highestScore2 = 0
    highestScore3 = 0
    highestScore4 = 0
    highestScore5 = 0
    counter1 = 0
    counter2 = 0
    counter3 = 0
    continent = ""

    # CALCULATING THE RELATIVE SCORE
    for country in TopUni["Country"]:
        if selectedCountry == country:
            university_score += TopUni["Score"][counter1]
            number_of_universities += 1
        counter1 += 1

    averageScore = university_score / number_of_universities

    for country in Capitals["Country Name"]:
        if selectedCountry == country:
            continent = Capitals["Continent"][counter2]
        counter2 += 1

    for continentScore in TopUni["Score"]:
        if TopUni["Country"][counter3] in ["Jordan", "Palestine", "China", "Israel", "Japan", "Singapore", "South Korea", "Taiwan"]:
            if continentScore > highestScore1:
                highestScore1 = continentScore
        elif TopUni["Country"][counter3] in "Australia":
            if continentScore > highestScore2:
                highestScore2 = continentScore
        elif TopUni["Country"][counter3] in ["Canada", "USA"]:
            if continentScore > highestScore3:
                highestScore3 = continentScore
        elif TopUni["Country"][counter3] in ["Denmark", "France", "Germany", "Netherlands", "Norway", "Sweden", "Switzerland", "United Kingdom"]:
            if continentScore > highestScore4:
                highestScore4 = continentScore
        elif TopUni["Country"][counter3] in ["Egypt"]:
            if continentScore > highestScore5:
                highestScore5 = continentScore

        counter3 += 1

    # PART 7 RELATIVE SCORE
    if selectedCountry in ["Jordan", "Palestine", "China", "Israel", "Japan", "Singapore", "South Korea", "Taiwan"]:
        relativeScore = (averageScore / highestScore1) * 100
        file.write("The relative score to the top university in {} is => ({} / {}) x 100% = {}%\n" .format(continent, averageScore, highestScore1, round(relativeScore, 1)))
    elif selectedCountry in "Australia":
        relativeScore = (averageScore / highestScore2) * 100
        file.write("The relative score to the top university in {} is => ({} / {}) x 100% = {}%\n" .format(continent, averageScore, highestScore2, round(relativeScore, 1)))
    elif selectedCountry in ["Canada", "USA"]:
        relativeScore = (averageScore / highestScore3) * 100
        file.write("The relative score to the top university in {} is => ({} / {}) x 100% = {}%\n" .format(continent, averageScore, highestScore3, round(relativeScore, 1)))
    elif selectedCountry in ["Denmark", "France", "Germany", "Netherlands", "Norway", "Sweden", "Switzerland", "United Kingdom"]:
        relativeScore = (averageScore / highestScore4) * 100
        file.write("The relative score to the top university in {} is => ({} / {}) x 100% = {}%\n" .format(continent, averageScore, highestScore4, round(relativeScore, 1)))
    elif selectedCountry in ["Egypt"]:
        relativeScore = (averageScore / highestScore5) * 100
        file.write("The relative score to the top university in {} is => ({} / {}) x 100% = {}%\n" .format(continent, averageScore, highestScore5, round(relativeScore, 1)))

    # FINDING THE CAPITAL OF THE SELECTED COUNTRY
    Capitals = pd.read_csv(capitalsFileName)
    capital = ""
    counter = 0

    for cap in Capitals["Country Name"]:
        if cap == selectedCountry:
            capital = Capitals["Capital"][counter]
        counter += 1

    file.write("The capital is => {}\n" .format(capital))  # PART 8 CAPITAL OF SELECTED COUNTRY

    # FINDING THE UNIVERSITIES THAT HAVE THE NAME OF THE CAPITAL WITHIN IT
    TopUni = pd.read_csv(rankingFileName)
    Capitals = pd.read_csv(capitalsFileName)
    capital = ""
    counter1 = 0
    counter2 = 0
    number_counter = 1
    for cap in Capitals["Country Name"]:
        if cap == selectedCountry:
            capital = Capitals["Capital"][counter1]
        counter1 += 1

    file.write("The universities that contain the capital name => \n")  # PART 9 CAPITAL NAME IN UNIVERSITY NAME

    for uni in TopUni["Country"]:
        if (selectedCountry == uni) and (capital in TopUni["Institution name"][counter2]):
            file.write("#" + str(number_counter) + " " + TopUni["Institution name"][counter2] + "\n")
            number_counter += 1
        counter2 += 1


def __main__():
    country = input("input the country you want to look at: ")
    file1 = "TopUni.csv"
    file2 = "capitals.csv"
    getInformation(country, file1, file2)

    
__main__()
