# Combine and format all data 

df["IndmetaId"] = list()
# FactID	Val	Year	Countries	Coutry_code	World_Regions	Zones	IndmetaID	Indmeta_text	ThemeID	Theme_text	Link	Reference

column_titles = ["Val","Year","Countries","Country_code", "World_Regions", "Zones","IndmetaID","Indmeta_text", "ThemeID", "Theme_text", "Link", "Reference", "Download Date"]
dfThememain.reindex(columns=column_titles)
