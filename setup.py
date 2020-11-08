from cx_Freeze import setup, Executable
import sys



files={"packages":["pygame"],
        "include_files":[
            "audio.wav",

            "enemyDown1.png",
            "enemyDown2.png",
            "enemyUp1.png",
            "enemyUp2.png",
            "enemyRight1.png",
            "enemyRight2.png",
            "enemyLeft1.png",
            "enemyLeft2.png",
            
            "playerDown1.png",
            "playerDown2.png",
            "playerUp1.png",
            "playerUp2.png",
            "playerRight1.png",
            "playerRight2.png",
            "playerLeft1.png",
            "playerLeft2.png",
            
            "playerAttackDown1.png",
            "playerAttackDown2.png",
            "playerAttackUp1.png",
            "playerAttackUp2.png",
            "playerAttackRight1.png",
            "playerAttackRight2.png",
            "playerAttackLeft1.png",
            "playerAttackLeft2.png", 
            "highScore.txt"         
        ]}
executable=Executable("main.py", base="Win32GUI", targetName="sampleGame.exe")

setup(
    name="Only One Action",
    version="0.1",
    author="Sean Crowley",
    description="ESU GameJam game",
    options={"build_exe": files},
    executables=[executable]
)