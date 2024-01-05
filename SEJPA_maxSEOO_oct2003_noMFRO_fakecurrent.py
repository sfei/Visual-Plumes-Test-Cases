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
ambient_depth0.current_speed = 1.6
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
    # csv_outputs(output_dict, "./outcsvs", "SEJPA_oct2003_noMFRO")
elif output_dict["error"]:
    print(output_dict["error"])
else:
    print("Unknown error")

# for debug comparisons

"""

Simulation:
Froude No: 21.92; 
Strat No:  6.76E-5; 
Spcg No:   36.00; 
k:         2.51E+5; 
eff den (sigmaT) -1.372976; 
eff vel          2.513(m/s);

         Depth    P-dia Ver angl  Polutnt  Density  P-speed   Dilutn   x-posn   Iso dia
Step      (ft)     (in)    (deg)    (ppb) (sigmaT)    (m/s)       ()     (ft)       (m)
   0     140.0    2.000      0.0   1200.0 -1.37298    2.513    1.000      0.0    0.0508;
   1     140.0    2.021   0.0174   1174.7 -0.80143    2.493    1.022   0.0245   0.05134; bottom hit;
  20     140.0    2.582    0.196    812.9  7.27599    2.213    1.476    0.335   0.06559;
  40     140.0    3.294    0.395    550.2  13.0495    2.013    2.181    0.858   0.08366;
  60     140.0    4.151    0.617    371.7  16.9393    1.878    3.229    1.745    0.1054;
  80     140.0    5.183    0.865    250.8  19.5620    1.787    4.785    3.279    0.1316;
 100     139.9    6.425    1.083    169.1  21.3301    1.726    7.098    5.649    0.1632;
 120     139.9    7.924    1.209    113.9  22.5217    1.685    10.54    8.871    0.2013;
 140     139.8    9.737    1.251    76.71  23.3245    1.657    15.64    13.11    0.2473;
 160     139.6    11.93    1.236    51.65  23.8651    1.639    23.23    18.67    0.3031;
 180     139.5    14.60    1.185    34.77  24.2292    1.626    34.51    26.00    0.3709;
 200     139.3    17.85    1.115    23.41  24.4743    1.618    51.27    35.75    0.4533;
 220     139.1    21.79    1.037    15.75  24.6393    1.612    76.17    48.74    0.5535;
 240     138.8    26.60    0.956    10.60  24.7503    1.608    113.2    66.12    0.6755;
 260     138.4    32.45    0.877    7.136  24.8250    1.605    168.2    89.42    0.8241;
 280     137.9    39.57    0.801    4.803  24.8753    1.604    249.9    120.7    1.0051;
 300     137.4    48.26    0.730    3.232  24.9092    1.603    371.3    162.7    1.2257;
 320     136.7    58.84    0.664    2.175  24.9320    1.602    551.7    219.2    1.4945;
 340     135.9    71.73    0.603    1.464  24.9473    1.601    819.7    295.2    1.8221;
 341     135.8    72.45    0.600    1.435  24.9479    1.601    836.1    299.7    1.8402; merging;
 360     134.7    92.19    0.568    0.985  24.9576    1.601   1218.1    411.9    2.3416;
 380     132.9    126.4    0.551    0.663  24.9646    1.601   1810.0    593.1    3.2096;
 400     130.3    179.9    0.542    0.446  24.9692    1.600   2689.5    866.4    4.5686; stream limit reached;
 420     126.5    261.6    0.550    0.300  24.9726    1.600   3996.4   1273.6    6.6449;
 440     120.6    384.8    0.793    0.202  24.9784    1.600   5938.4   1788.2    9.7735;
 452     115.8    486.4    0.947    0.159  24.9829    1.600   7531.3   2090.2    12.354; trap level;
 460     113.0    569.1    0.141    0.136  24.9778    1.600   8824.2   2384.1    14.455;
 461     113.2    579.4   -0.160    0.134  24.9768    1.600   8970.6   2463.4    14.718; local maximum rise or fall;
Horiz plane projections in effluent direction: radius(m):      0.0; CL(m):   750.87
Lmz(m):   750.87
forced entrain      1  4695.6   8.173   14.72   1.000

"""