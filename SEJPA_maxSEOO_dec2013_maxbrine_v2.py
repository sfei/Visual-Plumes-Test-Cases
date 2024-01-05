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
ambient_depth0.salinity      = 33.375
ambient_depth0.temperature   = 15.95
ambient_depth0.bg_conc       = 0
ambient_depth0.decay_rate    = 0
ambient_depth0.ff_velocity   = 0
ambient_depth0.ff_dir        = 0
ambient_depth0.ff_diff_coeff = 0
ambient_stack.append(ambient_depth0)

depths       = [3.0478, 6.0959, 9.1435, 12.1914, 15.2392, 18.2871, 21.3349, 24.3828, 27.4306, 30.4785, 33.5263, 36.5742,
                39.6221, 42.67]
salinities   = [0.375, 0.423, 0.445, 0.463, 0.436, 0.391, 0.307, 0.435, 0.313, 0.987-1, 0.962-1, 0.962-1, 0.0, 0.0]
temperatures = [15.946, 15.944, 15.938, 15.94, 15.878, 15.779, 15.604, 15.586, 15.2, 14.393, 14.036, 14.036, 14.0, 14.0]
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

Froude No: 40.98; 
Strat No:  4.78E-6; 
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
 330     129.2    76.27    65.27    32.58    14.11    16.20  24.3225    0.130    74.07    15.86    1.9373;
 345     125.9    83.88    69.46    32.64    14.10    13.78  24.3727    0.131    87.08    17.22    2.1306;
 360     120.5    95.86    73.61    32.71    14.08    11.25  24.4225    0.133    106.7    18.99    2.4349;
 375     110.8    117.5    77.72    32.77    14.07    8.579  24.4718    0.135    139.9    21.40    2.9856;
 390     96.04    155.1    80.61    32.82    14.11    6.375  24.5057    0.131    188.2    24.13    3.9391;
 405     75.64    191.3    83.60    32.95    14.40    4.737  24.5424    0.142    253.3    26.89    4.8596;
 420     47.59    283.6    84.57    33.06    14.73    3.519  24.5552    0.125    341.0    29.76    7.2036;
 434     9.462    393.1    85.51    33.15    15.02    2.667  24.5644    0.114    449.9    32.93    9.9844; trap level, matched energy radial vel = 0.0986m/s;
 435     6.159    409.0    85.44    33.15    15.04    2.615  24.5640    0.110    458.9    33.20    10.388;
 437    -0.971    453.6    85.17    33.16    15.08    2.513  24.5630   0.0998    477.4    33.79    11.521; surface;
 
Horiz plane projections in effluent direction: radius(m): 0.0; 
CL(m):   10.300
Lmz(m):  10.300
forced entrain      1     0.0   42.97   11.52  0.0817
Rate sec-1   0.0 
dy-1         0.0  
kt:          0.0
Amb Sal      33.3750
No farfield prediction when far vel = 0.

---- from text

Simulation:
Froude No: 40.98; 
Strat No:  4.78E-6; 
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
 330     126.6      0.0    70.20    32.44  24.2028    55.04    17.95      0.0    1.7830;
 345     122.0      0.0    79.90    32.52  24.2726    65.30    19.82      0.0    2.0295;
 360     114.9      0.0    95.71    32.61  24.3435    81.35    22.17      0.0    2.4311;
 375     103.0      0.0    122.3    32.70  24.4116    107.6    25.13      0.0    3.1071;
 390     85.86      0.0    162.4    32.81  24.4636    144.8    28.36      0.0    4.1259;
 405     63.31      0.0    215.0    32.95  24.5049    194.9    31.43      0.0    5.4622;
 420     31.02      0.0    302.1    33.07  24.5289    262.3    34.88      0.0    7.6726;
 428     9.040      0.0    363.6    33.12  24.5366    307.3    36.81      0.0    9.2357; matched energy radial vel =  0.130m/s;
 430     2.776      0.0    387.9    33.13  24.5368    319.8    37.34      0.0    9.8520; trap level;
 431    -0.542      0.0    402.5    33.14  24.5369    326.2    37.62      0.0    10.225; surface;
 
Horiz plane projections in effluent direction: radius(m):      0.0; 
CL(m):  11.467
Lmz(m): 11.467
forced entrain     1     0.0   42.84   10.22  0.0842
Rate sec-1   0.0 
dy-1         0.0  
kt:          0.0 
Amb Sal      33.3750
1:15:14 PM. amb fills: 4
"""