from visualplumes import units, Middleware, OutputUM3, Ambient, AmbientStore, ModelParameters, BacteriaModel, \
                         SimilarityProfile, MaxVerticalReversals, DiffuserParameters, DiffuserStore
from test_print_outputs import print_outputs
from test_convert_csv import csv_outputs
import numpy as np
from matplotlib import pyplot as plt


# initialize all parameter handlers

model_params  = ModelParameters()
diff_params   = DiffuserParameters()
diff_store    = DiffuserStore()
ambient_store = AmbientStore()

# model_parameters -- all should be same defaults except where indicated
model_params.report_effective_dillution = False
model_params.current_vector_averaging   = False
model_params.write_step_freq            = 15
model_params.max_reversals              = MaxVerticalReversals.MAX_RISE_OR_FALL
model_params.stop_on_bottom_hit         = False
model_params.dont_stop_on_surface_hit   = False
model_params.allow_induced_current      = False
model_params.max_dilution               = 10000
# model parameters (equation parameters)
model_params.contraction_coeff          = 0.61
model_params.light_absorb_coeff         = 0.16
model_params.aspiration_coeff           = 0.1
model_params.bacteria_model             = BacteriaModel.COLIFORM_MANCINI
model_params.at_equilibrium             = True
model_params.similarity_profile         = SimilarityProfile.DEFAULT
# model parameters (far-field model)
model_params.brooks_far_field           = True
model_params.tidal_pollution_buildup    = False
model_params.ff_increment               = 200
model_params.tpb_channel_width          = 100  # this TPB parameter is always required, even if no TPB modeled

# diffuser parameters
diff_params.diameter                 = 2
diff_store.diameter.units            = units.Length.INCHES
diff_params.offset_x                 = 0.0
diff_store.offset_x.units            = units.Length.METERS
diff_params.offset_y                 = 0.0
diff_store.offset_y.units            = units.Length.METERS
diff_params.vertical_angle           = 0
diff_store.vertical_angle.units      = units.Angle.DEGREES
diff_params.horizontal_angle         = 0
diff_store.horizontal_angle.units    = units.Angle.DEGREES
diff_params.num_ports                = 200
diff_store.num_ports.units           = units.Unitless.UNITLESS
diff_params.port_spacing             = 6
diff_store.port_spacing.units        = units.Length.FEET
diff_params.acute_mixing_zone        = 2000
diff_store.acute_mixing_zone.units   = units.Length.METERS
diff_params.isopleth                 = 0
diff_store.isopleth.units            = units.Isopleth.CONCENTRATION
diff_params.depth                    = 140
diff_store.depth.units               = units.Length.FEET
diff_params.effluent_flow            = 23.25
diff_store.effluent_flow.units       = units.FlowRate.MEGAGALLONS_PER_DAY
diff_params.salinity                 = 1.34
diff_store.salinity.units            = units.Salinity.PRACTICAL_SALINITY_UNITS
diff_params.temperature              = 22.5
diff_store.temperature.units         = units.Temperature.CELSIUS
diff_params.concentration            = 1200
diff_store.concentration.units       = units.Concentration.PARTS_PER_BILLION

# Setup ambient conditions
# All other ambient store parameters left at defaults, which are:
#    z_is_depth = True
#    extrapolation_sfc = Interpolation.CONSTANT
#    extrapolation_btm = Interpolation.CONSTANT
#    no time-series data
ambient_store.z.units             = units.Length.METERS
ambient_store.current_speed.units = units.Speed.METERS_PER_SECOND
ambient_store.current_dir.units   = units.Angle.DEGREES
ambient_store.salinity.units      = units.Salinity.PRACTICAL_SALINITY_UNITS
ambient_store.temperature.units   = units.Temperature.CELSIUS
ambient_store.bg_conc.units       = units.Concentration.KILOGRAM_PER_KILOGRAM
ambient_store.decay_rate.units    = units.DecayRate.PER_SECOND
ambient_store.ff_velocity.units   = units.Speed.METERS_PER_SECOND
ambient_store.ff_dir.units        = units.Angle.DEGREES
ambient_store.ff_diff_coeff.units = units.EddyDiffusivity.DIFFUSIVITY

ambient_stack = []

ambient_depth0 = Ambient()
ambient_depth0.z             = 0
ambient_depth0.current_speed = 0
ambient_depth0.current_dir   = 0
ambient_depth0.salinity      = 33.3757
ambient_depth0.temperature   = 15.95
ambient_depth0.bg_conc       = 0
ambient_depth0.decay_rate    = 0
ambient_depth0.ff_velocity   = 0
ambient_depth0.ff_dir        = 0
ambient_depth0.ff_diff_coeff = 0
ambient_stack.append(ambient_depth0)

depths       = [3.0478, 6.0959, 9.1435, 12.1914, 15.2392, 18.2871, 21.3349, 24.3828, 27.4306, 30.4785, 33.5263, 36.5742,
                39.6221, 42.67]
salinities   = [0.3757, 0.4233, 0.445, 0.4633, 0.436, 0.391, 0.307, 0.435, 0.313, 0.987, 0.962, 0.962, 0.0, 0.0]
temperatures = [15.946, 15.944, 15.938, 15.941, 15.878, 15.779, 15.604, 15.586, 15.2, 14.393, 14.036, 14.036, 14.0, 14.0]
for i, depth in enumerate(depths):
    ambient_depth_x = Ambient()
    ambient_depth_x.z             = depth
    ambient_depth_x.salinity      = 33.0 + salinities[i]
    ambient_depth_x.temperature   = temperatures[i]
    ambient_stack.append(ambient_depth_x)

# Setup outputs handler
output_handler = OutputUM3()
# Add parameters to outputs: regime     parameter name    label        unit class           unit type
output_handler.add_parameter('element', 'depth',          'Depth',     units.Length,        diff_store.depth.units)
output_handler.add_parameter('element', 'diameter',       'Diameter',  units.Length,        diff_store.diameter.units)
output_handler.add_parameter('element', 'vertical_angle', 'V-angle',   units.Angle,         units.Angle.DEGREES)
output_handler.add_parameter('element', 'salinity',       'Salinity',  units.Salinity,      ambient_store.salinity.units)
output_handler.add_parameter('element', 'temperature',    'Temp.',     units.Temperature,   ambient_store.temperature.units)
output_handler.add_parameter('element', 'concentration',  'Pollutant', units.Concentration, diff_store.concentration.units)
output_handler.add_parameter('element', 'density',        'Density',   units.Density,       units.Density.SIGMA_T)
output_handler.add_parameter('ambient', 'density',        'Amb-den',   units.Density,       units.Density.SIGMA_T)
# output_handler.add_parameter('ambient', 'salinity',       'Amb-sal',   units.Salinity,      ambient_store.salinity.units)
# output_handler.add_parameter('ambient', 'temperature',    'Amb-temp',  units.Temperature,   ambient_store.temperature.units)
output_handler.add_parameter('element', 'dilution',       'Dilution',  units.Unitless,      units.Unitless.UNITLESS)
output_handler.add_parameter('element', 'speed',          'Velocity',  units.Speed,         ambient_store.current_speed.units)
output_handler.add_parameter('element', 'x_displacement', 'X-pos',     units.Length,        units.Length.FEET)
# output_handler.add_parameter('element', 'mass',           'Mass',      units.Mass,          units.Mass.KILOGRAMS)
# output_handler.add_parameter('element', 'd_mass',         'Entrained', units.Mass,          units.Mass.KILOGRAMS)
# output_handler.add_parameter('model',   'um3isoplet',     'Isopleth',  units.Unitless,      units.Unitless.UNITLESS)

# setup and run model

output_dict = Middleware.run(
    model_params=model_params,
    diffuser_params=diff_params,
    diffuser_store=diff_store,
    timeseries_handler=None,
    ambient_stack=ambient_stack,
    ambient_store=ambient_store,
    output_handler=output_handler
)


# this is for debugging purposes -- can show plots like
#   profile plot  -> plot('trajectory', 'boundary1', 'boundary2', flip_y=True)
#   plan plot     -> plot('path', 'out1', 'out2')
#   density plot  -> plot('density', 'ambdensity', flip_y=True)
#   dilution plot -> plot('dilution', 'cldilution')
# etc.
def _plot(series_name, color):
    coords = output_dict["graphs"][series_name]["coords"]
    coords = np.array(coords).astype(float)
    plt.plot(coords[:,0], coords[:,1], linewidth=1, color=color, alpha=0.2)
    plt.scatter(coords[:,0], coords[:,1], s=1, color=color)
def plot(series_name, series_name_2=None, series_name_3=None, flip_y=False):
    _plot(series_name, "black")
    if series_name_2:
        _plot(series_name_2, "blue")
    if series_name_3:
        _plot(series_name_3, "green")
    if flip_y:
        plt.gca().invert_yaxis()
    plt.show()

# print outputs and handle errors
if output_dict and output_dict["success"]:
    print_outputs(output_dict)
    plot('trajectory', 'boundary1', 'boundary2', flip_y=True)
    csv_outputs(output_dict, "./outcsvs", "SEJPA_dec2013_maxbrine")
elif output_dict["error"]:
    print(output_dict["error"])
else:
    print("Unknown error")

# for debug comparisons

"""
---- from model

Simulation:

Froude No: 40.98; 
Strat No:  4.76E-6; 
Spcg No:   46.09; 
k:         4.12E+5; 
eff den (sigmaT) -1.267032;
eff vel          4.119(m/s);
Current is very small, flow regime may be transient.

         Depth    P-dia Ver angl  Eff-sal     Temp  Polutnt  Density  P-speed   Dilutn   x-posn   Iso dia
Step      (ft)     (in)    (deg)    (psu)      (C)    (ppb) (sigmaT)    (m/s)       ()     (ft)       (m)
   0     140.0    1.562      0.0    1.340    22.50   1200.0 -1.26703    4.119    1.000      0.0   0.03968;
   1     140.0    1.656   0.0106    4.928    21.54   1067.1  1.67149    3.653    1.125    0.036   0.04207; bottom hit;
  15     140.0    2.292   0.0498    11.73    19.71    813.2  7.22767    2.768    1.476    0.150   0.05822;
  30     140.0    3.078    0.124    17.19    18.24    606.9  11.6947    2.057    1.977    0.312   0.07818;
  45     140.0    4.136    0.259    21.25    17.15    452.4  15.0168    1.528    2.652    0.531    0.1050;
  60     140.0    5.559    0.502    24.27    16.34    337.0  17.4889    1.136    3.561    0.827    0.1412;
  75     140.0    7.475    0.944    26.52    15.74    250.8  19.3286    0.844    4.784    1.225    0.1899;
  90     140.0    10.05    1.743    28.18    15.29    186.6  20.6975    0.627    6.430    1.761    0.2553;
 105     139.9    13.51    3.187    29.42    14.96    138.8  21.7158    0.467    8.645    2.481    0.3433;
 120     139.9    18.15    5.782    30.34    14.71    103.2  22.4731    0.348    11.63    3.449    0.4611;
 135     139.7    23.78    9.893    30.98    14.54    78.62  22.9961    0.267    15.26    4.620    0.6040;
 150     139.5    28.56    14.18    31.32    14.45    65.11  23.2832    0.225    18.43    5.622    0.7253;
 165     139.2    32.68    18.47    31.55    14.39    56.35  23.4695    0.199    21.30    6.506    0.8301;
 180     138.9    36.40    22.75    31.71    14.35    49.92  23.6060    0.181    24.04    7.320    0.9246;
 195     138.6    39.86    27.02    31.85    14.31    44.84  23.7140    0.169    26.76    8.093    1.0124;
 210     138.1    43.15    31.30    31.96    14.28    40.58  23.8045    0.159    29.57    8.845    1.0960;
 225     137.6    46.36    35.57    32.05    14.25    36.87  23.8834    0.152    32.55    9.592    1.1776;
 240     137.1    49.58    39.83    32.14    14.23    33.51  23.9548    0.146    35.81    10.35    1.2592;
 255     136.4    52.88    44.09    32.22    14.21    30.39  24.0211    0.142    39.49    11.12    1.3431;
 270     135.5    56.39    48.34    32.29    14.19    27.42  24.0841    0.138    43.76    11.93    1.4323;
 285     134.5    60.25    52.59    32.37    14.17    24.54  24.1454    0.135    48.90    12.78    1.5304;
 300     133.2    64.69    56.83    32.44    14.15    21.69  24.2058    0.133    55.32    13.71    1.6431;
 315     131.5    70.02    61.06    32.52    14.13    18.85  24.2663    0.130    63.67    14.72    1.7785;
 320     130.8    72.08    62.46    32.54    14.12    17.90  24.2865    0.130    67.06    15.08    1.8309; merging;
 330     129.2    76.20    65.30    32.58    14.11    16.21  24.3228    0.130    74.01    15.85    1.9355;
 345     126.7    79.94    69.61    32.65    14.10    14.29  24.3793    0.137    84.00    16.87    2.0304;
 360     123.9    81.79    73.88    32.75    14.09    12.55  24.4535    0.151    95.61    17.79    2.0776;
 375     120.1    83.41    78.11    32.90    14.08    10.67  24.5696    0.173    112.5    18.72    2.1187;
 390     113.5    90.07    82.03    33.14    14.07    8.254  24.7572    0.199    145.4    19.82    2.2879;
 405     103.9    107.3    84.44    33.35    14.07    6.134  24.9206    0.212    195.6    20.91    2.7247;
 418     92.85    135.8    85.44    33.47    14.16    4.742  24.9953    0.200    253.1    21.86    3.4504; trap level;
 420     90.74    145.6    85.36    33.47    14.19    4.558  24.9911    0.188    263.3    22.03    3.6982;
 435     78.63    352.7    81.14    33.46    14.35    3.913  24.9473    0.085    306.7    23.33    8.9596;
 441     77.38    438.6    79.29    33.46    14.36    3.883  24.9450   0.0699    309.0    23.54    11.142; begin overlap;
 450     76.44    558.8    76.57    33.46    14.36    3.872  24.9442   0.0558    309.9    23.75    14.193;
 465     75.74    748.6    72.10    33.46    14.36    3.870  24.9440   0.0421    310.1    23.94    19.015;
 480     75.42    931.4    67.67    33.46    14.36    3.870  24.9440   0.0341    310.1    24.06    23.657;
 495     75.25   1107.5    63.28    33.46    14.36    3.870  24.9440   0.0288    310.1    24.14    28.130;
 510     75.14   1276.4    58.90    33.46    14.36    3.870  24.9440   0.0251    310.1    24.19    32.420;
 525     75.08   1437.3    54.53    33.46    14.36    3.870  24.9440   0.0223    310.1    24.24    36.509;
 540     75.03   1589.6    50.18    33.46    14.36    3.870  24.9440   0.0202    310.1    24.27    40.376;
 555     75.00   1732.5    45.83    33.46    14.36    3.870  24.9440   0.0186    310.1    24.30    44.004;
 570     74.98   1865.1    41.49    33.46    14.36    3.870  24.9440   0.0173    310.1    24.33    47.374;
 585     74.96   1986.9    37.16    33.46    14.36    3.870  24.9440   0.0162    310.1    24.35    50.468;
 600     74.94   2097.3    32.83    33.46    14.36    3.870  24.9440   0.0154    310.1    24.37    53.271;
 604     74.94   2124.7    31.68    33.46    14.36    3.870  24.9440   0.0152    310.1    24.37    53.967; surface;


Horiz plane projections in effluent direction: radius(m): 0.0; 
CL(m):   7.4284
Lmz(m):  7.4284
forced entrain      1     0.0   19.83   53.97   0.848
Rate sec-1   0.0 
dy-1         0.0  
kt:          0.0 
Amb Sal      33.3703
No farfield prediction when far vel = 0.

---- from text

Simulation:
Froude No: 40.98; 
Strat No:  4.76E-6; 
Spcg No:   14.05; 
k:         4.12E+5; 
eff den (sigmaT) -1.267032; 
eff vel          4.119(m/s);
Current is very small, flow regime may be transient.

        Depth  Amb-cur    P-dia  Eff-sal  Density   Dilutn   x-posn   y-posn   Iso dia
Step     (ft)    (m/s)     (in)    (psu) (sigmaT)       ()     (ft)     (ft)       (m)
   0     140.0 1.000E-5    1.562    1.340 -1.26703    1.000      0.0      0.0   0.03968;
   1     140.0      0.0    1.656    4.928  1.67149    1.125    0.036      0.0   0.04207; bottom hit;
  15     140.0      0.0    2.292    11.73  7.22767    1.476    0.150      0.0   0.05822;
  30     140.0      0.0    3.078    17.19  11.6947    1.977    0.312      0.0   0.07818;
  45     140.0      0.0    4.136    21.25  15.0168    2.652    0.531      0.0    0.1050;
  60     140.0      0.0    5.559    24.27  17.4889    3.561    0.827      0.0    0.1412;
  75     140.0      0.0    7.475    26.52  19.3286    4.784    1.225      0.0    0.1899;
  90     140.0      0.0    10.05    28.18  20.6975    6.430    1.761      0.0    0.2553;
 105     139.9      0.0    13.51    29.42  21.7158    8.645    2.481      0.0    0.3433;
 120     139.9      0.0    18.15    30.34  22.4731    11.63    3.449      0.0    0.4611;
 130     139.8      0.0    21.97    30.81  22.8571    14.09    4.244      0.0    0.5580; merging;
 135     139.7      0.0    23.70    30.96  22.9863    15.17    4.621      0.0    0.6019;
 150     139.5      0.0    27.92    31.26  23.2333    17.79    5.645      0.0    0.7091;
 165     139.2      0.0    31.46    31.45  23.3910    19.99    6.574      0.0    0.7991;
 180     138.9      0.0    34.63    31.60  23.5078    22.00    7.454      0.0    0.8796;
 195     138.5      0.0    37.56    31.71  23.6018    23.94    8.309      0.0    0.9541;
 210     138.0      0.0    40.35    31.81  23.6822    25.90    9.159      0.0    1.0250;
 225     137.4      0.0    43.07    31.89  23.7539    27.93    10.02      0.0    1.0940;
 240     136.7      0.0    45.79    31.97  23.8203    30.12    10.91      0.0    1.1630;
 255     135.9      0.0    48.59    32.05  23.8837    32.56    11.84      0.0    1.2341;
 270     134.9      0.0    51.57    32.13  23.9456    35.35    12.83      0.0    1.3100;
 285     133.5      0.0    54.91    32.20  24.0074    38.67    13.90      0.0    1.3946;
 300     131.9      0.0    58.82    32.28  24.0704    42.75    15.08      0.0    1.4939;
 315     129.6      0.0    63.67    32.36  24.1353    47.97    16.41      0.0    1.6171;
 330     127.0      0.0    68.30    32.44  24.2064    54.03    17.73      0.0    1.7348;
 345     124.1      0.0    71.53    32.55  24.2922    60.86    18.92      0.0    1.8169;
 360     120.5      0.0    74.27    32.70  24.4084    69.73    20.09      0.0    1.8865;
 375     115.1      0.0    79.32    32.92  24.5790    84.30    21.41      0.0    2.0147;
 390     105.4      0.0    95.15    33.18  24.7849    112.7    23.09      0.0    2.4168;
 405     92.55      0.0    125.7    33.36  24.9060    151.6    24.70      0.0    3.1931;
 406     91.53      0.0    129.6    33.36  24.9059    154.6    24.82      0.0    3.2923; trap level;
 420     74.65      0.0    277.2    33.37  24.8602    194.5    27.12      0.0    7.0404;
 435     69.73      0.0    453.3    33.37  24.8512    201.3    28.12      0.0    11.515; begin overlap;
 450     68.16      0.0    602.6    33.37  24.8500    202.2    28.58      0.0    15.306;
 465     67.40      0.0    743.2    33.37  24.8498    202.3    28.87      0.0    18.876;
 480     66.98      0.0    878.1    33.37  24.8498    202.3    29.07      0.0    22.303;
 495     66.72      0.0   1007.2    33.37  24.8498    202.3    29.22      0.0    25.584;
 510     66.54      0.0   1130.2    33.37  24.8498    202.4    29.34      0.0    28.706;
 525     66.43      0.0   1246.3    33.37  24.8498    202.4    29.43      0.0    31.657;
 540     66.34      0.0   1355.1    33.37  24.8498    202.4    29.51      0.0    34.419;
 555     66.28      0.0   1455.9    33.37  24.8498    202.4    29.58      0.0    36.980;
 570     66.23      0.0   1548.3    33.37  24.8498    202.4    29.64      0.0    39.327;
 585     66.20      0.0   1631.7    33.37  24.8498    202.4    29.69      0.0    41.446;
 600     66.17      0.0   1705.8    33.37  24.8498    202.4    29.74      0.0    43.328;
 610     66.15      0.0   1749.8    33.37  24.8498    202.4    29.77      0.0    44.445; surface;
 
Horiz plane projections in effluent direction: radius(m):      0.0; 
CL(m):  9.0739
Lmz(m): 9.0739
forced entrain      1     0.0   22.51   44.45   0.905
Rate sec-1   0.0 
dy-1         0.0  
kt:          0.0 
Amb Sal      33.3393
11:06:27 AM. amb fills: 4
"""