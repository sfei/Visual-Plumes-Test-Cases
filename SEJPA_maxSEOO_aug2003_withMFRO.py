from visualplumes import units, Middleware, OutputUM3, Ambient, AmbientStore, ModelParameters, BacteriaModel, \
                         SimilarityProfile, MaxVerticalReversals, DiffuserParameters, DiffuserStore
from test_print_outputs import print_outputs


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
ambient_depth0.salinity      = 33.4
ambient_depth0.temperature   = 20
ambient_depth0.bg_conc       = 0
ambient_depth0.decay_rate    = 0
ambient_depth0.ff_velocity   = 0
ambient_depth0.ff_dir        = 0
ambient_depth0.ff_diff_coeff = 0
ambient_stack.append(ambient_depth0)

depths       = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42.67]
salinities   = [0.56, 0.60, 0.54, 0.56, 0.53, 0.53, 0.50, 0.51, 0.51, 0.50, 0.51, 0.48, 0.48, 0.48]
temperatures = [18.73, 15.20, 14.35, 13.32, 12.67, 12.04, 11.75, 11.68, 11.54, 11.44, 11.34, 11.35, 11.35, 11.35]
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

print_outputs(output_dict)

# for debug comparisons

"""
---- from model

Froude No: 40.30; 
Strat No:  6.89E-5; 
Spcg No:   46.09; 
k:         4.12E+5; 
eff den (sigmaT) -1.267032; 
eff vel          4.119(m/s);
Current is very small, flow regime may be transient.

         Depth    P-dia  Eff-sal     Temp  Polutnt  Density  P-speed   Dilutn   x-posn   Iso dia
Step      (ft)     (in)    (psu)      (C)    (ppb) (sigmaT)    (m/s)       ()     (ft)       (m)
   0     140.0    1.562    1.340    22.50   1200.0 -1.26703    4.119    1.000      0.0   0.03968;
   1     140.0    1.656    4.986    21.24   1067.1  1.78383    3.652    1.125   0.0359   0.04207; bottom hit;
  15     140.0    2.292    11.88    18.84    813.4  7.53961    2.768    1.475    0.150   0.05821;
  30     140.0    3.077    17.43    16.92    607.1  12.1603    2.057    1.976    0.312   0.07817;
  45     140.0    4.135    21.56    15.49    452.6  15.5933    1.528    2.651    0.531    0.1050;
  60     140.0    5.558    24.62    14.42    337.2  18.1464    1.135    3.559    0.826    0.1412;
  75     140.0    7.473    26.90    13.63    251.0  20.0455    0.844    4.781    1.224    0.1898;
  90     140.0    10.05    28.59    13.05    186.7  21.4583    0.627    6.426    1.760    0.2552;
 105     139.9    13.51    29.85    12.61    138.9  22.5090    0.467    8.639    2.480    0.3432;
 120     139.9    18.14    30.78    12.29    103.3  23.2904    0.348    11.62    3.447    0.4609;
 135     139.7    23.68    31.42    12.07    78.97  23.8234    0.269    15.20    4.598    0.6015;
 150     139.5    28.34    31.77    11.94    65.61  24.1163    0.227    18.29    5.578    0.7198;
 165     139.2    32.38    32.00    11.87    56.86  24.3079    0.201    21.10    6.444    0.8224;
 180     138.9    36.03    32.16    11.81    50.43  24.4489    0.183    23.80    7.243    0.9151;
 195     138.6    39.42    32.30    11.76    45.32  24.5609    0.171    26.48    8.003    1.0013;
 210     138.1    42.66    32.41    11.72    41.03  24.6548    0.161    29.25    8.743    1.0835;
 225     137.7    45.82    32.51    11.69    37.27  24.7370    0.154    32.19    9.478    1.1638;
 240     137.1    48.98    32.60    11.66    33.88  24.8114    0.148    35.42    10.22    1.2442;
 255     136.4    52.24    32.68    11.63    30.72  24.8806    0.144    39.07    10.98    1.3270;
 270     135.5    55.71    32.76    11.60    27.71  24.9465    0.140    43.31    11.78    1.4151;
 285     134.5    59.54    32.83    11.57    24.78  25.0106    0.137    48.42    12.63    1.5124;
 300     133.2    63.95    32.91    11.55    21.89  25.0739    0.135    54.82    13.54    1.6242;
 315     131.5    69.25    32.98    11.52    19.00  25.1372    0.132    63.16    14.54    1.7591;
 322     130.5    72.18    33.02    11.51    17.64  25.1669    0.131    68.01    15.05    1.8334; merging;
 330     129.2    75.61    33.06    11.50    16.26  25.1972    0.131    73.81    15.67    1.9206;
 345     126.0    82.98    33.12    11.48    13.83  25.2504    0.133    86.78    16.99    2.1078;
 360     120.9    93.63    33.18    11.45    11.36  25.3044    0.137    105.6    18.63    2.3782;
 375     112.2    111.5    33.25    11.43    8.778  25.3618    0.141    136.7    20.77    2.8318;
 390     98.81    138.6    33.32    11.41    6.522  25.4151    0.146    184.0    23.11    3.5204;
 405     80.46    183.5    33.37    11.44    4.846  25.4481    0.143    247.6    25.47    4.6611;
 420     53.81    271.5    33.40    11.53    3.601  25.4601    0.124    333.3    28.20    6.8966; trap level;
 434     39.74    576.4    33.42    11.64    3.248  25.4508    0.063    369.4    29.86    14.642; begin overlap;
 435     39.55    596.6    33.42    11.64    3.246  25.4506   0.0611    369.7    29.90    15.154;
 450     38.09    880.5    33.42    11.64    3.239  25.4502   0.0424    370.5    30.21    22.364;
 465     37.60   1149.0    33.42    11.64    3.239  25.4502   0.0328    370.5    30.36    29.185;
 480     37.36   1407.6    33.42    11.64    3.239  25.4502    0.027    370.5    30.45    35.754;
 495     37.23   1656.4    33.42    11.64    3.239  25.4502    0.023    370.5    30.52    42.072;
 503     37.19   1784.7    33.42    11.64    3.239  25.4502   0.0214    370.5    30.54    45.332; surface;
 
Horiz plane projections in effluent direction: radius(m):  0.0; 
CL(m):   9.3098
Lmz(m):  9.3098
forced entrain      1     0.0   31.34   45.33   0.502
Rate sec-1   0.0 
dy-1         0.0  
kt:          0.0 
Amb Sal      33.5556
No farfield prediction when far vel = 0.

---- from text

Simulation:
Froude No: 40.30; 
Strat No:  6.89E-5; 
Spcg No:   14.05; 
k:         4.12E+5; 
eff den (sigmaT) -1.267032; 
eff vel          4.119(m/s);

Current is very small, flow regime may be transient.
        Depth  Amb-cur    P-dia  Eff-sal  Density   Dilutn   x-posn   y-posn   Iso dia
Step     (ft)    (m/s)     (in)    (psu) (sigmaT)       ()     (ft)     (ft)       (m)
   0     140.0 1.000E-5    1.562    1.340 -1.26703    1.000      0.0      0.0   0.03968;
   1     140.0      0.0    1.656    4.986  1.78383    1.125   0.0359      0.0   0.04207; bottom hit;
  15     140.0      0.0    2.292    11.88  7.53961    1.475    0.150      0.0   0.05821;
  30     140.0      0.0    3.077    17.43  12.1603    1.976    0.312      0.0   0.07817;
  45     140.0      0.0    4.135    21.56  15.5933    2.651    0.531      0.0    0.1050;
  60     140.0      0.0    5.558    24.62  18.1464    3.559    0.826      0.0    0.1412;
  75     140.0      0.0    7.473    26.90  20.0455    4.781    1.224      0.0    0.1898;
  90     140.0      0.0    10.05    28.59  21.4583    6.426    1.760      0.0    0.2552;
 105     139.9      0.0    13.51    29.85  22.5090    8.639    2.480      0.0    0.3432;
 120     139.9      0.0    18.14    30.78  23.2904    11.62    3.447      0.0    0.4609;
 131     139.8      0.0    22.28    31.29  23.7133    14.29    4.307      0.0    0.5659; merging;
 135     139.7      0.0    23.60    31.41  23.8142    15.11    4.599      0.0    0.5996;
 150     139.5      0.0    27.73    31.71  24.0666    17.68    5.598      0.0    0.7043;
 165     139.2      0.0    31.20    31.90  24.2287    19.84    6.508      0.0    0.7924;
 180     138.9      0.0    34.30    32.04  24.3493    21.83    7.369      0.0    0.8712;
 195     138.5      0.0    37.17    32.16  24.4467    23.75    8.208      0.0    0.9442;
 210     138.0      0.0    39.91    32.26  24.5301    25.68    9.042      0.0    1.0137;
 225     137.4      0.0    42.57    32.35  24.6047    27.70    9.888      0.0    1.0814;
 240     136.8      0.0    45.24    32.43  24.6738    29.88    10.76      0.0    1.1491;
 255     135.9      0.0    47.99    32.51  24.7398    32.30    11.68      0.0    1.2189;
 270     134.9      0.0    50.93    32.59  24.8044    35.09    12.65      0.0    1.2936;
 285     133.6      0.0    54.22    32.66  24.8690    38.40    13.71      0.0    1.3771;
 300     131.9      0.0    58.08    32.74  24.9348    42.49    14.87      0.0    1.4753;
 315     129.7      0.0    62.89    32.82  25.0026    47.73    16.18      0.0    1.5975;
 330     126.7      0.0    69.27    32.91  25.0734    54.77    17.69      0.0    1.7594;
 345     122.3      0.0    78.34    33.00  25.1476    64.79    19.47      0.0    1.9899;
 360     115.6      0.0    92.38    33.09  25.2254    80.13    21.65      0.0    2.3466;
 375     104.6      0.0    114.8    33.19  25.3073    105.2    24.33      0.0    2.9169;
 390     88.88      0.0    150.6    33.27  25.3710    141.5    27.17      0.0    3.8258;
 405     67.26      0.0    206.9    33.33  25.4095    190.5    30.11      0.0    5.2545;
 414     49.99      0.0    262.9    33.36  25.4184    227.6    32.10      0.0    6.6781; trap level;
 420     36.99      0.0    367.6    33.38  25.4096    252.5    33.70      0.0    9.3376;
 430     32.65      0.0    581.3    33.38  25.4045    258.3    34.41      0.0    14.765; begin overlap;
 435     31.92      0.0    667.7    33.38  25.4039    258.8    34.57      0.0    16.960;
 450     30.85      0.0    911.3    33.38  25.4036    259.0    34.85      0.0    23.146;
 465     30.40      0.0   1144.2    33.38  25.4036    259.0    35.01      0.0    29.063;
 480     30.17      0.0   1368.4    33.38  25.4036    259.0    35.12      0.0    34.758;
 490     30.07      0.0   1512.9    33.38  25.4036    259.0    35.17      0.0    38.428; surface;
 
Horiz plane projections in effluent direction: radius(m): 0.0; 
CL(m): 10.719
Lmz(m): 10.719
forced entrain      1     0.0   33.51   38.43   0.481
Rate sec-1   0.0 
dy-1         0.0  
kt:          0.0 
Amb Sal      33.5411
"""