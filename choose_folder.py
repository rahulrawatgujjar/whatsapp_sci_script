dirs=[
    "Canon_Ixus55_0",
    "Canon_Ixus70_0",
    "Canon_PowerShotA640",
    "Nikon_CoolPixS710_0",
    "Nikon_D200",
    "Nikon_D70",
    "Sony_DSC_H50",
    "Sony_DSC_T77",
    "Sony_DSC_W170",
    "Agfa_DC-504_0",
    "Agfa_DC-733s",
    "Agfa_DC-830i_0"
]

def get_folder():
  for i in range(1,13):
    print(f"{i} --> {dirs[i-1]}")
  x=int(input("\nChoose the folder by picking a number: "))
  if not 1<=x<=12:
    raise ValueError("Number should be in range 1 to 12")
  print(f"\nDid you choose: {dirs[x-1]}")
  isTrue=input("\nEnter y or n :")
  if isTrue not in ("y","Y","yes","Yes"):
    print("Run the code again !!!")
    return
  return dirs[x-1]
