# filter out names with unwanted words
# split into two databases -> those with websites and those without
# search for keywords for those with websites and tag -> if broken link, move to no website
# somehow deal with those without websites -> google search???


filter = ["jehova", "jehova's witness", "mormon", "latter day", "latter day saints", "joseph smith", "lds", "god the mother", 
          "jéhova", "mormone", "mormonisme", "saints des derniers jours", "derniers jours", "dieu la mère"]

nolink = []