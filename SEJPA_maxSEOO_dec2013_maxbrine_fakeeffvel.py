from visualplumes import units, Middleware, OutputUM3, Ambient, AmbientStore, ModelParameters, BacteriaModel, \
                         SimilarityProfile, MaxVerticalReversals, DiffuserParameters, DiffuserStore
from test_print_outputs import print_outputs
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
diff_params.effluent_flow            = 80
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
    # csv_outputs(output_dict, "./outcsvs", "SEJPA_oct2003_noMFRO")
elif output_dict["error"]:
    print(output_dict["error"])
else:
    print("Unknown error")

# for debug comparisons

"""

Simulation:
Froude No: 141.0; 
Strat No:  4.76E-6; 
Spcg No:   46.09; 
k:         1.42E+6; 
eff den (sigmaT) -1.267032; 
eff vel          14.17(m/s);
Current is very small, flow regime may be transient.

         Depth    P-dia Ver angl     Temp  Polutnt  Density  P-speed   Dilutn   x-posn   y-posn   Iso dia
Step      (ft)     (in)    (deg)      (C)    (ppb) (sigmaT)    (m/s)       ()     (ft)     (ft)       (m)
   0     140.0    1.562      0.0    22.50   1200.0 -1.26703    14.17    1.000      0.0      0.0   0.03968;
   1     140.0    1.867  0.00307    19.90    840.0  6.64454    9.845    1.429   0.0969      0.0   0.04742; bottom hit;
  15     140.0    2.921  0.00849    18.47    639.4  10.9942    7.461    1.877    0.244      0.0   0.07418;
  30     140.0    3.924   0.0187    17.32    476.7  14.4957    5.544    2.517    0.452      0.0   0.09967;
  45     140.0    5.274   0.0372    16.47    355.1  17.1011    4.119    3.379    0.732      0.0    0.1340;
  60     140.0    7.092   0.0708    15.84    264.4  19.0400    3.060    4.539    1.109      0.0    0.1801;
  75     140.0    9.538    0.132    15.36    196.7  20.4828    2.274    6.101    1.618      0.0    0.2423;
  90     140.0    12.83    0.242    15.01    146.3  21.5561    1.690    8.202    2.302      0.0    0.3259;
 105     140.0    17.26    0.441    14.75    108.8  22.3543    1.255    11.03    3.224      0.0    0.4384;
 120     140.0    23.22    0.802    14.56    80.88  22.9479    0.933    14.84    4.465      0.0    0.5899;
 135     139.9    31.24    1.456    14.42    60.12  23.3892    0.693    19.96    6.135      0.0    0.7936;
 150     139.9    42.03    2.639    14.31    44.69  23.7173    0.516    26.85    8.382      0.0    1.0676;
 165     139.7    56.50    4.771    14.23    33.21  23.9612    0.384    36.13    11.40      0.0    1.4350;
 178     139.3    72.81    7.910    14.18    25.71  24.1205    0.299    46.67    14.81      0.0    1.8495; merging;
 180     139.2    75.43    8.482    14.17    24.91  24.1375    0.290    48.17    15.36      0.0    1.9160;
 195     138.5    92.90    12.77    14.15    21.27  24.2149    0.251    56.43    19.13      0.0    2.3597;
 210     137.6    108.2    17.06    14.13    19.13  24.2603    0.230    62.73    22.57      0.0    2.7473;
 225     136.4    122.1    21.34    14.12    17.58  24.2933    0.217    68.28    25.85      0.0    3.1009;
 240     135.0    135.0    25.62    14.11    16.32  24.3199    0.209    73.51    29.06      0.0    3.4303;
 255     133.3    147.3    29.89    14.11    15.25  24.3427    0.203    78.69    32.27      0.0    3.7423;
 270     131.3    159.2    34.16    14.10    14.28  24.3633    0.199    84.03    35.54      0.0    4.0432;
 285     128.8    170.5    38.49    14.09    13.40  24.3828    0.197    89.58    38.83      0.0    4.3296;
 300     126.7    175.8    42.86    14.09    12.77  24.4029    0.201    93.94    41.28      0.0    4.4653;
 315     124.7    176.9    47.19    14.09    12.27  24.4250    0.208    97.79    43.24      0.0    4.4929;
 330     122.7    175.5    51.50    14.08    11.80  24.4510    0.218    101.7    44.97      0.0    4.4570;
 345     120.5    172.3    55.79    14.08    11.34  24.4835    0.232    105.9    46.60      0.0    4.3775;
 360     117.8    168.6    60.04    14.08    10.81  24.5255    0.249    111.0    48.26      0.0    4.2823;
 375     114.0    167.2    64.26    14.08    10.12  24.5813    0.268    118.5    50.25      0.0    4.2475;
 390     108.3    170.4    68.46    14.07    9.201  24.6559    0.289    130.4    52.73      0.0    4.3290;
 405     98.72    183.4    72.62    14.09    7.954  24.7526    0.307    150.9    56.04      0.0    4.6573;
 413     88.49    210.6    74.02    14.18    6.934  24.7893    0.290    173.0    59.03      0.0    5.3485; trap level;
 420     75.09    285.9    72.78    14.34    6.037  24.7729    0.235    198.8    63.04      0.0    7.2621;
 435     58.28    468.9    68.23    14.48    5.365  24.7532    0.167    223.7    68.91      0.0    11.911;
 450     50.03    609.8    63.85    14.54    5.152  24.7470    0.135    232.9    72.57      0.0    15.490;
 465     45.00    736.0    59.47    14.56    5.047  24.7442    0.114    237.7    75.29      0.0    18.695;
 467     44.48    751.9    58.89    14.57    5.038  24.7439    0.112    238.2    75.60      0.0    19.099; begin overlap;
 480     41.73    848.3    55.11    14.58    4.999  24.7429    0.101    240.0    77.39      0.0    21.547;
 495     39.50    947.9    50.76    14.58    4.980  24.7424   0.0906    241.0    79.08      0.0    24.077;
 501     38.80    985.2    49.02    14.58    4.976  24.7423   0.0873    241.2    79.67      0.0    25.025; ceiling;
 510     37.92   1038.8    46.41    14.58    4.971  24.7422    0.083    241.4    80.47      0.0    26.386;
 525     36.79   1122.1    42.06    14.59    4.967  24.7420    0.077    241.6    81.63      0.0    28.502;
 531     36.43   1153.4    40.33    14.59    4.966  24.7420    0.075    241.7    82.05      0.0    29.296; surface;
 
Horiz plane projections in effluent direction: radius(m):      0.0; 
CL(m):   25.010
Lmz(m):  25.010
"""