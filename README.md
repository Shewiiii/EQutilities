Random repo containing B&K 5128's frequency responses and some tools to help EQing IEMs.
(Important note: I'm still learning Python so the code is very dirty)

# How to use
**This repo can be useful if you want to Equalize an IEM to sound like another IEM without buying a new one**, or simply if you want to analyse a Frequency Response in depth. It should be used with [Listener's Graph Database](https://listener800.github.io/5128?share=Custom_Tilt&bass=0&tilt=-1&treble=0&ear=0) (the B&K 5128 one), since it has more advanced features (and no paywalls) to work with Frequency Response than [Crinacle's Database](https://crinacle.com/graphs/iems/graphtool/?share=Diffuse_Field_Target&tilt=-1&tool=4620) or [squig.link](https://squig.link/), such as Y-axis scale adjustment, more preferences adjustements to the target, or the JM-1 target (which a [more suitable target to use for IEMs](https://youtu.be/xKOrHq_7Uw4?si=P1KXwkYhuMucot58&t=350)).

> [!WARNING]
> More measurments available will be added in the future. It is also worth noting that the B&K 5128, while being the most accurate measurment rig available today, is expensive and has only been standardized recently, so relatively few measurements are available. 

## AutoEQ an IEM to another IEM
### With a preset (recommended)
#### Currently Compatible apps:
- Wavelet
- Poweramp
- Poweramp Equalizer
- HQPlayer (IIR plugin)
- (Parametric EQ apps, you have to enter the values manually)

Many auto-generated EQs are available in the `presets` folder:
1. If available, click on the folder of the IEM you want to EQ.
2. Click on the folder corresponding to the EQ format you want (if you are using Peace or another parametric EQ software, select `Parametric`, if you are using HQPlayer, select `IIR`).
3. Download the file of the IEM you want to EQ to.
4. Import the file (or copy the values if Parametric) in your EQ app.
5. Done!
### Manually
In order to do this, follow [these steps](https://github.com/Shewiiii/EQutilities/blob/main/README.md#autoeq-an-iem-to-a-chosen-target), but instead of using the default targets, you can import the Frequency Response of an IEM, which can be used as a target in the `Equalizer` tab. Click on `Upload Target`, then you can AutoEQ.
> [!IMPORTANT]
> You may want to EQ the treble region by ear. The difference in HRTF with you and the measurment rig will probably result in a different Frequency Response between the graph and the the acutal sound to your eardums.

## Import and visualize the Frequency Response of an IEM
1. Download the txt file in the `frequency_responses` folder of the IEM you want.
2. Open [Listener's Graph Database](https://listener800.github.io/5128?share=Custom_Tilt&bass=0&tilt=-1&treble=0&ear=0).
3. Click on `Equalizer`, then on `Upload FR`.
4. Select the txt file.
5. (Optional) Adjust the level of the Frequency Response by using the arrows on the new entry.
6. Choose the target with the settings you want.
7. Done!
> [!TIP]
> The JM-1 with a -1dB/octave tilt can be considered as neutral for most people and is a great target to start. But while the JM-1 target (as well as the "5128 DF target") is a target based on objective data (Diffuse Field + Mixed HRTF compensation), the population average pinna effect and the 5128's canal effect are NOT the same as your ears. Thus, the target should be adjusted with a tilt that fits your own hearing (and preferences).

## AutoEQ an IEM to a chosen target
1. Open [Listener's Graph Database](https://listener800.github.io/5128?share=Custom_Tilt&bass=0&tilt=-1&treble=0&ear=0).
2. Import the Frequency Response of the IEM you want to EQ (see the paragraph above)
3. Adjust the target to your liking with the `5128 Target` and `Preferences Adjustments` panels
4. In the `Equalizer` tab, adjust the settings to your liking and click `AutoEQ`
5. Import the generated values in your EQ software
6. Done!
> [!TIP]
> Adding more filters by clicking on the `+` button will result in an Equalization closer to the target. If the loading screen gets stucked, remove the `extra-eq-overlay` div in the source code of the website. Change the frequency range to 20-20000hz to EQ the full audible range.

## Import your EQ profile in Poweramp/Poweramp Equalizer manually
1. Copy the repo.
2. On [Listener's Graph Database](https://listener800.github.io/5128?share=Custom_Tilt&bass=0&tilt=-1&treble=0&ear=0), click on `Export Parametric EQ` to export the EQ profile you have just made, and save it in the `input_ParaEQ` folder.
3. Open `paraToJSONconverter(Poweramp).py` and edit the `file` variable to the name of the file you have saved.
4. Run the file. A JSON file will be created in the `output_JSON` folder.
5. Import the file in Poweramp: in the app, go to the Equalizer tab, then click on the 3 dots. You can import your file from here.
6. Done!
> [!IMPORTANT]
> If you are using Poweramp Equalizer, switch the `Band Overlap` setting to `Cascade`.

## Import your EQ profile in HQPlayer 4 or 5 manually
1. Copy the repo.
2. On [Listener's Graph Database](https://listener800.github.io/5128?share=Custom_Tilt&bass=0&tilt=-1&treble=0&ear=0), click on `Export Parametric EQ` to export the EQ profile you have just made, and save it in the `input_ParaEQ` folder.
3. Open `paraToIIRconverter.py` and edit the `file` variable to the name of the file you have saved.
4. Run the file. A txt file will be created in the `output_IIR` folder, and the EQ string will be displayed in the console.
5. Copy the string in HQPlayer: in the software, click on `Matrix`, then `Pipeline setup...`
6. In the first 2 raws, copy the string in the `Process` column
7. Put de pre-gain value in the `Gain` column
8. In the text zone, put the name of your EQ profile, then hit Save.
9. Done!

The `FR_C_Scraper` and `FR_L_Scraper` files are the files im using to scrap the Frequency response from Crinacle and Listener's database (so the FR can be used as a target as well).
