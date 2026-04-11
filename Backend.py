import pandas as pds
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# Calculation
def tinh_TDEE(can_nang, chieu_cao, tuoi, gioi_tinh, van_dong, muc_tieu):
    if gioi_tinh == "Nam":
        TDEE = (10 * can_nang) + (6.25 * chieu_cao) - (5 * tuoi) + 5
    else:
        TDEE = (10 * can_nang) + (6.25 * chieu_cao) - (5 * tuoi) + 161
    if van_dong == "Rất hay vận động":
        TDEE = TDEE * 1.725
    elif van_dong == "Hay vận động":
        TDEE = TDEE * 1.55
    elif van_dong == "Ít vận động":
        TDEE = TDEE * 1.375
    else:
        TDEE = TDEE * 1.2
    if muc_tieu == "Tăng cân":
        TDEE += 375
    elif muc_tieu == "Giảm cân":
        TDEE -= 500
    return round(TDEE)
def tinh_protein(can_nang, muc_tieu, van_dong):
    if van_dong == "Rất hay vận động":
        if muc_tieu == "Tăng cân" or "Giảm cân":
            protein = can_nang * 2.2
        else:
            protein = can_nang * 2
    elif van_dong == "Hay vận động":
        if muc_tieu == "Tăng cân" or "Giảm cân":
            protein = can_nang * 1.8
        else:
            protein = can_nang * 1.6
    elif van_dong == "Ít vận động":
        if muc_tieu == "Tăng cân" or "Giảm cân":
            protein = can_nang * 1.4
        else:
            protein = can_nang * 1.2
    else:
        if muc_tieu in ["Tăng cân", "Giảm cân"]:
            protein = can_nang * 1.2
        else:
            protein = can_nang * 1
    return round(protein)
def tinh_fat(calo_muc_tieu):
    fat_can_thiet = (calo_muc_tieu * 0.3)/9
    return round(fat_can_thiet)
def tinh_carb(calo_muc_tieu, protein_can_thiet, fat_can_thiet):
    carb_can_thiet = (calo_muc_tieu - protein_can_thiet * 4 - fat_can_thiet * 9)/4
    return round(carb_can_thiet)
# KNN
def learn(file_csv):
    df = pds.read_csv("duantinhoc.csv")
    features = ["Protein (g)", "Carbs (g)", "Fat (g)", "Calo (kcal)"]
    Imp_features = df[features]
    scaler = StandardScaler()
    Imp_features_scaled = scaler.fit_transform(Imp_features)
    knn = NearestNeighbors(metric = "euclidean")
    knn.fit(Imp_features_scaled)
    return knn, df, scaler
def create(knn, df, scaler, calo_muc_tieu, carb_can_thiet, protein_can_thiet, fat_can_thiet):
    carb_meal = carb_can_thiet / 3
    protein_meal = protein_can_thiet / 3
    fat_meal = fat_can_thiet / 3
    calo_meal = calo_muc_tieu / 3
    meal = [[carb_meal, protein_meal, fat_meal, calo_meal]]
    meal_scaled = scaler.transform(meal)
    _, indicies = knn.kneighbors(meal_scaled, n_neighbors = 3)
    menu = []
    for mon in range(3):
        i_mon_an = indicies[0][mon]
        mon_an = df.iloc[i_mon_an]
        menu.append(mon_an)
    return menu
