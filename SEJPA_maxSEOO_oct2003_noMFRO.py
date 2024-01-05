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
model_params.current_vector_averaging   = True
model_params.write_step_freq            = 20
model_params.max_reversals              = MaxVerticalReversals.MAX_RISE_OR_FALL
model_params.stop_on_bottom_hit         = False
model_params.dont_stop_on_surface_hit   = False
model_params.allow_induced_current      = False
model_params.max_dilution               = 10000
# model parameters (equation parameters)
model_params.contraction_coeff          = 1.0
model_params.light_absorb_coeff         = 0.16
model_params.aspiration_coeff           = 0.1
model_params.bacteria_model             = BacteriaModel.COLIFORM_MANCINI
model_params.at_equilibrium             = True
model_params.similarity_profile         = SimilarityProfile.DEFAULT
# model parameters (far-field model)
model_params.brooks_far_field           = False
model_params.tidal_pollution_buildup    = True
model_params.tpb_channel_width          = 39.6  # all units assumed meters or degrees
model_params.tpb_segment_length         = 80.46
model_params.tpb_upstream_dir           = 180
model_params.tpb_coast_bin              = 65
model_params.tpb_coast_concentration    = 9e-6
model_params.tpb_mixing_zone_ceil       = 3.657

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
diff_params.salinity                 = 1.2
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
ambient_depth0.salinity      = 33.32
ambient_depth0.temperature   = 20.09
ambient_depth0.bg_conc       = 0
ambient_depth0.decay_rate    = 0
ambient_depth0.ff_velocity   = 0
ambient_depth0.ff_dir        = 0
ambient_depth0.ff_diff_coeff = 0
ambient_stack.append(ambient_depth0)

depths       = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42.67]
salinities   = [0.32, 0.32, 0.24, 0.2, 0.14, 0.09, 0.09, 0.12, 0.12, 0.12, 0.15, 0.17, 0.13, 0.13]
temperatures = [20.01, 19.9, 18.92, 18.11, 17.18, 16.08, 15.59, 14.58, 13.93, 13.88, 13.76, 12.96, 12.95, 12.95]
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
# output_handler.add_parameter('element', 'salinity',       'Salinity',  units.Salinity,      ambient_store.salinity.units)
# output_handler.add_parameter('element', 'temperature',    'Temp.',     units.Temperature,   ambient_store.temperature.units)
output_handler.add_parameter('element', 'concentration',  'Pollutant', units.Concentration, diff_store.concentration.units)
output_handler.add_parameter('element', 'density',        'Density',   units.Density,       units.Density.SIGMA_T)
# output_handler.add_parameter('ambient', 'density',        'Amb-den',   units.Density,       units.Density.SIGMA_T)
# output_handler.add_parameter('ambient', 'salinity',       'Amb-sal',   units.Salinity,      ambient_store.salinity.units)
# output_handler.add_parameter('ambient', 'temperature',    'Amb-temp',  units.Temperature,   ambient_store.temperature.units)
output_handler.add_parameter('element', 'dilution',       'Dilution',  units.Unitless,      units.Unitless.UNITLESS)
output_handler.add_parameter('element', 'speed',          'Velocity',  units.Speed,         ambient_store.current_speed.units)
output_handler.add_parameter('element', 'x_displacement', 'X-pos',     units.Length,        units.Length.FEET)
# output_handler.add_parameter('element', 'y_displacement', 'Y-pos',     units.Length,        units.Length.FEET)
# output_handler.add_parameter('element', 'mass',           'Mass',      units.Mass,          units.Mass.KILOGRAMS)
# output_handler.add_parameter('element', 'd_mass',         'Entrained', units.Mass,          units.Mass.KILOGRAMS)
output_handler.add_parameter('model',    'iso_diameter',  'Iso diameter', units.Length,     diff_store.diameter.units)

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
    csv_outputs(output_dict, "./outcsvs", "SEJPA_oct2003_noMFRO")
elif output_dict["error"]:
    print(output_dict["error"])
else:
    print("Unknown error")

# for debug comparisons

"""
---- from model
Simulation:
Froude No: 21.92; 
Strat No:  6.76E-5; 
Spcg No:   36.00; 
k:         2.51E+5; 
eff den (sigmaT) -1.372976; 
eff vel          2.513(m/s);
Current is very small, flow regime may be transient.

         Depth    P-dia Ver angl  Polutnt  Density  P-speed   Dilutn   x-posn   Iso dia
Step      (ft)     (in)    (deg)    (ppb) (sigmaT)    (m/s)       ()     (ft)       (m)
   0     140.0    2.000      0.0   1200.0 -1.37298    2.513    1.000      0.0    0.0508;
   1     140.0    2.058   0.0177   1132.8  0.14227    2.369    1.059   0.0233   0.05229; bottom hit;
  20     140.0    3.047    0.201    783.6  7.92153    1.626    1.531    0.219   0.07738;
  40     140.0    4.514    0.618    530.3  13.4841    1.094    2.263    0.523    0.1147;
  60     140.0    6.695    1.537    358.2  17.2323    0.737    3.350    0.975    0.1701;
  80     140.0    9.929    3.561    241.6  19.7595    0.496    4.966    1.647    0.2522;
 100     139.9    14.67    7.931    163.2  21.4559    0.337    7.351    2.635    0.3726;
 120     139.7    19.27    13.65    123.6  22.3118    0.260    9.707    3.595    0.4894;
 140     139.4    23.01    19.36    102.2  22.7747    0.221    11.74    4.397    0.5845;
 160     139.1    26.30    25.07    87.70  23.0874    0.198    13.68    5.123    0.6680;
 180     138.8    29.34    30.77    76.62  23.3263    0.182    15.66    5.813    0.7452;
 200     138.3    32.27    36.46    67.44  23.5245    0.171    17.79    6.494    0.8196;
 220     137.7    35.22    42.14    59.35  23.6991    0.164    20.22    7.188    0.8945;
 240     137.0    38.36    47.82    51.88  23.8603    0.158    23.13    7.915    0.9742;
 260     136.0    41.90    53.48    44.71  24.0148    0.153    26.84    8.700    1.0644;
 280     134.7    46.23    59.12    37.64  24.1673    0.150    31.88    9.571    1.1742;
 300     132.8    51.97    64.75    30.52  24.3208    0.146    39.31    10.57    1.3202;
 320     129.9    60.45    70.35    23.30  24.4766    0.141    51.51    11.76    1.5355;
 338     125.6    72.70    75.30    16.82  24.6167    0.135    71.35    13.07    1.8466; merging;
 340     124.9    74.40    75.86    16.18  24.6308    0.135    74.19    13.24    1.8897;
 360     115.5    94.22    80.88    10.92  24.7495    0.140    109.9    15.10    2.3932;
 380     99.27    148.0    82.64    7.347  24.7877    0.117    163.3    17.33    3.7604;
 383     95.69    163.7    82.64    6.923  24.7878    0.110    173.3    17.79    4.1583; trap level;
 400     77.28    357.3    79.04    5.568  24.7809   0.0598    215.5    20.38    9.0762;
 403     76.77    392.9    78.11    5.550  24.7804    0.055    216.2    20.48    9.9790; begin overlap;
 420     75.50    572.0    72.97    5.531  24.7797   0.0385    217.0    20.80    14.530;
 440     75.02    768.3    67.06    5.530  24.7797   0.0289    217.0    20.97    19.515;
 460     74.81    954.6    61.20    5.530  24.7797   0.0234    217.0    21.07    24.246;
 480     74.70   1130.0    55.37    5.530  24.7797   0.0199    217.0    21.14    28.702;
 500     74.63   1293.2    49.56    5.530  24.7797   0.0174    217.0    21.19    32.847;
 520     74.59   1442.8    43.77    5.530  24.7797   0.0156    217.0    21.23    36.646;
 540     74.56   1577.4    37.99    5.530  24.7797   0.0143    217.0    21.26    40.065;
 560     74.54   1695.7    32.22    5.530  24.7797   0.0133    217.0    21.29    43.072;
 568     74.54   1738.3    29.91    5.530  24.7797    0.013    217.0    21.30    44.153; ceiling;
 580     74.53   1796.8    26.45    5.530  24.7797   0.0126    217.0    21.31    45.639;
 600     74.52   1879.6    20.70    5.530  24.7797   0.0121    217.0    21.33    47.743;
 605     74.52   1897.4    19.26    5.530  24.7797    0.012    217.0    21.34    48.194; surface;
 
Horiz plane projections in effluent direction: radius(m):   0.0; 
CL(m):   6.5040
Lmz(m):  6.5040

---- from text

Froude No:  40.65; 
Strat No:   5.28E-5; 
Spcg No:    14.05; 
k:          4.12E+5; 
eff den (sigmaT) -1.372976; 
eff vel          4.119(m/s);
Current is very small, flow regime may be transient.

         Depth  Amb-cur    P-dia  Eff-sal  Density   Dilutn   x-posn   y-posn   Iso dia
Step      (ft)    (m/s)     (in)    (psu) (sigmaT)       ()     (ft)     (ft)       (m)
   0     140.0 1.000E-5    1.562    1.200 -1.37298    1.000      0.0      0.0   0.03968;
   1     140.0      0.0    1.656    4.820  1.61719    1.125   0.0359      0.0   0.04207; bottom hit;
  15     140.0      0.0    2.292    11.67  7.26602    1.475    0.150      0.0   0.05821;
  30     140.0      0.0    3.078    17.19  11.8052    1.977    0.312      0.0   0.07817;
  45     140.0      0.0    4.135    21.29  15.1800    2.652    0.531      0.0    0.1050;
  60     140.0      0.0    5.558    24.33  17.6907    3.560    0.827      0.0    0.1412;
  75     140.0      0.0    7.474    26.59  19.5589    4.783    1.224      0.0    0.1898;
  90     140.0      0.0    10.05    28.27  20.9489    6.428    1.760      0.0    0.2553;
 105     139.9      0.0    13.51    29.52  21.9828    8.643    2.481      0.0    0.3432;
 120     139.9      0.0    18.15    30.45  22.7518    11.62    3.448      0.0    0.4610;
 131     139.8      0.0    22.31    30.95  23.1704    14.31    4.314      0.0    0.5668; merging;
 135     139.7      0.0    23.66    31.07  23.2704    15.15    4.610      0.0    0.6009;
 150     139.5      0.0    27.83    31.37  23.5199    17.74    5.622      0.0    0.7068;
 165     139.2      0.0    31.33    31.57  23.6797    19.92    6.541      0.0    0.7958;
 180     138.9      0.0    34.47    31.71  23.7983    21.92    7.412      0.0    0.8755;
 195     138.5      0.0    37.37    31.82  23.8939    23.85    8.259      0.0    0.9493;
 210     138.0      0.0    40.14    31.92  23.9757    25.79    9.101      0.0    1.0194;
 225     137.4      0.0    42.83    32.01  24.0488    27.82    9.955      0.0    1.0878;
 240     136.8      0.0    45.52    32.09  24.1166    30.00    10.84      0.0    1.1562;
 255     135.9      0.0    48.29    32.17  24.1812    32.43    11.76      0.0    1.2266;
 270     134.9      0.0    51.26    32.25  24.2444    35.22    12.74      0.0    1.3019;
 285     133.6      0.0    54.57    32.32  24.3076    38.54    13.81      0.0    1.3860;
 300     131.9      0.0    58.45    32.40  24.3719    42.62    14.98      0.0    1.4847;
 315     129.7      0.0    63.28    32.48  24.4383    47.85    16.30      0.0    1.6074;
 330     126.6      0.0    69.67    32.56  24.5075    54.87    17.82      0.0    1.7697;
 345     122.3      0.0    78.48    32.65  24.5804    64.70    19.58      0.0    1.9933;
 360     115.9      0.0    91.44    32.75  24.6581    79.41    21.68      0.0    2.3226;
 375     104.1      0.0    123.2    32.85  24.7162    105.9    24.67      0.0    3.1283;
 390     85.67      0.0    187.8    32.92  24.7351    142.6    28.61      0.0    4.7709;
 392     82.53      0.0    199.7    32.93  24.7356    148.3    29.24      0.0    5.0726; trap level;
 405     71.32      0.0    335.5    32.95  24.7251    166.6    31.73      0.0    8.5217;
 411     70.33      0.0    381.5    32.95  24.7234    167.8    32.02      0.0    9.6893; begin overlap;
 420     69.42      0.0    444.7    32.95  24.7223    168.4    32.32      0.0    11.294;
 435     68.60      0.0    542.6    32.95  24.7219    168.6    32.66      0.0    13.782;
 450     68.14      0.0    635.5    32.95  24.7218    168.7    32.88      0.0    16.142;
 465     67.86      0.0    724.2    32.95  24.7218    168.7    33.05      0.0    18.395;
 480     67.68      0.0    808.4    32.95  24.7218    168.7    33.18      0.0    20.534;
 495     67.55      0.0    887.8    32.95  24.7218    168.7    33.29      0.0    22.550;
 510     67.46      0.0    961.9    32.95  24.7218    168.7    33.38      0.0    24.433;
 525     67.39      0.0   1030.4    32.95  24.7218    168.7    33.45      0.0    26.172;
 540     67.34      0.0   1092.9    32.95  24.7218    168.7    33.52      0.0    27.761;
 555     67.30      0.0   1149.2    32.95  24.7218    168.7    33.58      0.0    29.189;
 570     67.27      0.0   1198.8    32.95  24.7218    168.7    33.64      0.0    30.450;
 585     67.24      0.0   1241.6    32.95  24.7218    168.7    33.69      0.0    31.537;
 600     67.23      0.0   1277.3    32.95  24.7218    168.7    33.74      0.0    32.445;
 615     67.21      0.0   1305.8    32.95  24.7218    168.7    33.78      0.0    33.168;
 630     67.20      0.0   1326.9    32.95  24.7218    168.7    33.83      0.0    33.704;
 645     67.20      0.0   1340.5    32.95  24.7218    168.7    33.87      0.0    34.049;
 660     67.20      0.0   1346.5    32.95  24.7218    168.7    33.91      0.0    34.202;
 663     67.20      0.0   1346.8    32.95  24.7218    168.7    33.92      0.0    34.210; local maximum rise or fall;
 
Horiz plane projections in effluent direction: radius(m):      0.0; 
CL(m):   10.339
Lmz(m):  10.339

"""