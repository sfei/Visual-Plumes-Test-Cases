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
model_params.write_step_freq            = 100   # might be adjusted down for debugging purposes (default=100)
model_params.max_reversals              = MaxVerticalReversals.SECOND_MAX_RISE_OR_FALL
model_params.stop_on_bottom_hit         = False
model_params.dont_stop_on_surface_hit   = False
model_params.allow_induced_current      = False
model_params.max_dilution               = 10000  # might be adjusted down for debugging purposes
# model parameters (equation parameters)
model_params.contraction_coeff          = 1.0
model_params.light_absorb_coeff         = 0.16
model_params.aspiration_coeff           = 0.1
model_params.bacteria_model             = BacteriaModel.COLIFORM_MANCINI
model_params.at_equilibrium             = True  # true means equation of state considers S,T (no pressure)
model_params.similarity_profile         = SimilarityProfile.DEFAULT
# model parameters (far-field model)
model_params.brooks_far_field           = False
model_params.tidal_pollution_buildup    = False
model_params.tpb_channel_width          = 10000  # this TPB parameter is always required, even if no TPB modeled

# diffuser parameters
diff_params.diameter                 = 0.05
diff_store.diameter.units            = units.Length.METERS
diff_params.offset_x                 = 0.0
diff_store.offset_x.units            = units.Length.METERS
diff_params.offset_y                 = 0.0
diff_store.offset_y.units            = units.Length.METERS
diff_params.vertical_angle           = 20
diff_store.vertical_angle.units      = units.Angle.DEGREES
diff_params.horizontal_angle         = 0
diff_store.horizontal_angle.units    = units.Angle.N_DEGREES
diff_params.num_ports                = 1
diff_store.num_ports.units           = units.Unitless.UNITLESS
diff_params.acute_mixing_zone        = 100
diff_store.acute_mixing_zone.units   = units.Length.METERS
diff_params.isopleth                 = 0
diff_store.isopleth.units            = units.Isopleth.CONCENTRATION
diff_params.depth                    = 49
diff_store.depth.units               = units.Length.METERS
diff_params.effluent_flow            = 0.05
diff_store.effluent_flow.units       = units.FlowRate.MEGAGALLONS_PER_DAY
diff_params.salinity                 = 0
diff_store.salinity.units            = units.Salinity.PRACTICAL_SALINITY_UNITS
diff_params.temperature              = 25
diff_store.temperature.units         = units.Temperature.CELSIUS
diff_params.concentration            = 100
diff_store.concentration.units       = units.Concentration.PARTS_PER_MILLION

# Setup ambient conditions
# All other ambient store parameters left at defaults, which are:
#    z_is_depth = True
#    extrapolation_sfc = Interpolation.CONSTANT
#    extrapolation_btm = Interpolation.CONSTANT
#    no time-series data
ambient_store.current_speed.units = units.Speed.METERS_PER_SECOND
ambient_store.current_dir.units   = units.Angle.DEGREES
ambient_store.salinity.units      = units.Salinity.PRACTICAL_SALINITY_UNITS
ambient_store.temperature.units   = units.Temperature.CELSIUS
ambient_store.bg_conc.units       = units.Concentration.PARTS_PER_MILLION
ambient_store.decay_rate.units    = units.DecayRate.PER_SECOND
ambient_store.ff_velocity.units   = units.Speed.METERS_PER_SECOND
ambient_store.ff_dir.units        = units.Angle.DEGREES
ambient_store.ff_diff_coeff.units = units.EddyDiffusivity.DIFFUSIVITY
# Two depth layers at 0 and 50m, with only surface conditions defined
# (with constant extrapolation to bottom, basically assumes constant conditions to depth)
ambient_depth0 = Ambient()
ambient_depth0.z             = 0
ambient_depth0.current_speed = 0.1
ambient_depth0.current_dir   = 90
ambient_depth0.salinity      = 33
ambient_depth0.temperature   = 15
ambient_depth0.bg_conc       = 0
ambient_depth0.decay_rate    = 0
ambient_depth0.ff_velocity   = 0
ambient_depth0.ff_dir        = 0
ambient_depth0.ff_diff_coeff = 0.0003
# Note that default values are None in Ambient class. This means values will be interpolated / extrapolated.
ambient_depth50 = Ambient()
ambient_depth50.z = 50
# Create stack for passing to model in order of shallowest to deepest
ambient_stack = (ambient_depth0, ambient_depth50)

# Setup outputs handler
# This may not be supplied to UMUnit, in which case default parameters will be tracked. But this is how you can
# explicitly track variables of interest, specifying the units you want the outputs in. The order that parameters are
# added will be the same as the order of values in the output list. You do also need to know the `regime` and var name,
# so the output handler knows where to grab the values from. This may have to come from a hard-coded list of allowed
# vars to track, so I will have to provide it for UI later.
output_handler = OutputUM3()
# Add parameters to outputs: regime     parameter name    label        unit class           unit type
output_handler.add_parameter('element', 'depth',          'Depth',     units.Length,        diff_store.depth.units)
output_handler.add_parameter('element', 'diameter',       'Width',     units.Length,        diff_store.diameter.units)
output_handler.add_parameter('element', 'vertical_angle', 'V-angle',   units.Angle,         diff_store.vertical_angle.units)
output_handler.add_parameter('element', 'salinity',       'Salinity',  units.Salinity,      ambient_store.salinity.units)
output_handler.add_parameter('element', 'temperature',    'Temp.',     units.Temperature,   ambient_store.temperature.units)
output_handler.add_parameter('element', 'concentration',  'Pollutant', units.Concentration, diff_store.concentration.units)
output_handler.add_parameter('element', 'density',        'Density',   units.Density,       units.Density.SIGMA_T)
# output_handler.add_parameter('ambient', 'density',       'Amb-den',  units.Density,       units.Density.SIGMA_T)
# output_handler.add_parameter('ambient', 'current_speed', 'Amb-cur',  units.Speed,         ambient_store.current_speed.units)
output_handler.add_parameter('element', 'speed',          'Velocity',  units.Speed,         ambient_store.current_speed.units)
output_handler.add_parameter('element', 'dilution',       'Dilution',  units.Unitless,      units.Unitless.UNITLESS)
output_handler.add_parameter('element', 'x_displacement', 'X-pos',     units.Length,        units.Length.METERS)
output_handler.add_parameter('element', 'y_displacement', 'Y-pos',     units.Length,        units.Length.METERS)
output_handler.add_parameter('element', 'mass',           'Mass',      units.Mass,          units.Mass.KILOGRAMS)
output_handler.add_parameter('element', 'd_mass',         'Entrained', units.Mass,          units.Mass.KILOGRAMS)

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
TEXT OUTPUT FROM YUCCA:

Ambient Table:
     Depth   Amb-cur   Amb-dir   Amb-sal   Amb-tem   Amb-pol     Decay   Far-spd   Far-dir   Disprsn   Density
         m       m/s       deg       psu         C     kg/kg       s-1       m/s       deg  m0.67/s2   sigma-T
       0.0     0.100     90.00     33.00     15.00       0.0       0.0       0.0       0.0    0.0003  24.45518
     50.00     0.100     90.00     33.00     15.00       0.0       0.0       0.0       0.0    0.0003  24.45518

Diffuser table:
   P-diaVer angl H-Angle SourceX SourceY   Ports  MZ-dis Isoplth P-depth Ttl-flo Eff-sal    Temp Polutnt
     (m)   (deg)(Surv-deg)     (m)     (m)      ()     (m)(concent)     (m)   (MGD)   (psu)     (C)   (ppm)
  0.0500  20.000     0.0     0.0     0.0  1.0000  100.00     0.0  49.000  0.0500     0.0  25.000  100.00

Froude No:  9.620; 
Strat No:   0.0000; 
Spcg No:    4.28E+9; 
k:          11.16; 

        Depth     P-dia Ver angl  Eff-sal     Temp  Polutnt  Density  P-speed   Dilutn   y-posn   Iso dia
Step      (m)       (m)    (deg)    (psu)      (C)    (ppm) (sigmaT)    (m/s)       ()      (m)       (m)
   0     49.00    0.050    20.00      0.0    25.00    100.0 -2.89272    1.116    1.000      0.0    0.0500;
 100     48.75    0.277    26.18    28.47    16.37    14.06  20.6837    0.257    7.113    0.599    0.2767;
 200     47.94    1.029    28.92    32.37    15.19    1.947  23.9337    0.135    51.37    2.037    1.0291;
 300     46.13    3.088    19.47    32.91    15.03    0.269  24.3832    0.109    372.0    6.232    3.0879;
 400     41.70    8.560    11.91    32.99    15.00   0.0371  24.4452    0.103   2694.8    23.35    8.5601;
 467     35.23    16.73    8.534    33.00    15.00  0.00985  24.4525    0.101  10156.3    60.67    16.729; stop dilution reached;

Horiz plane projections in effluent direction: radius(m):  0.0
CL(m):   60.671
Lmz(m):  60.671
forced entrain      1 2.69E+11   13.77   16.73   0.989
Rate sec-1          0.0 dy-1          0.0  kt:          0.0 Amb Sal      33.0000

        Depth   Amb-cur    P-dia Ver angl  H-Angle  Eff-sal     Temp  Polutnt  Density  P-speed   Dilutn   x-posn   y-posn   Iso dia
Step      (m)     (m/s)      (m)    (deg)(Surv-deg)   (psu)      (C)    (ppm) (sigmaT)    (m/s)       ()      (m)      (m)       (m)
   0     49.00    0.100    0.050    20.00      0.0      0.0    25.00    100.0 -2.89272    1.116    1.000      0.0      0.0    0.0500;
   1     49.00    0.100   0.0506    19.99      0.0    0.811    24.75    97.61 -2.21876    1.091    1.025      0.0  0.00308   0.05061;
   2     49.00    0.100   0.0517    19.99      0.0    1.442    24.56    95.74 -1.69447    1.072    1.044    0.000  0.00551   0.05168;
   3     49.00    0.100   0.0526    19.98      0.0    2.061    24.38    93.92 -1.18066    1.053    1.065    0.000  0.00787   0.05265;
   4     49.00    0.100   0.0536    19.98      0.0    2.668    24.19    92.12 -0.67710    1.034    1.086    0.000   0.0103   0.05363;
   5     49.00    0.100   0.0546    19.97      0.0    3.262    24.01    90.36 -0.18359    1.016    1.107    0.000   0.0128   0.05464;
   6     48.99    0.100   0.0557    19.97      0.0    3.845    23.83    88.63  0.30009    0.998    1.128    0.000   0.0153   0.05566;
   7     48.99    0.100   0.0567    19.97      0.0    4.417    23.66    86.93  0.77414    0.980    1.150    0.000   0.0178    0.0567;
   8     48.99    0.100   0.0578    19.96      0.0    4.978    23.49    85.27  1.23877    0.963    1.173    0.000   0.0205   0.05776;
   9     48.99    0.100   0.0588    19.96      0.0    5.527    23.33    83.63  1.69415    0.946    1.196    0.000   0.0231   0.05884;
  10     48.99    0.100   0.0599    19.96      0.0    6.066    23.16    82.03  2.14050    0.930    1.219    0.000   0.0258   0.05994;
  11     48.99    0.100   0.0611    19.96      0.0    6.594    23.00    80.46  2.57800    0.914    1.243    0.000   0.0286   0.06106;
  12     48.99    0.100   0.0622    19.96      0.0    7.112    22.84    78.91  3.00682    0.898    1.267    0.000   0.0314   0.06219;
  13     48.99    0.100   0.0634    19.96      0.0    7.619    22.69    77.40  3.42715    0.882    1.292    0.000   0.0343   0.06335;
  14     48.99    0.100   0.0645    19.96      0.0    8.117    22.54    75.91  3.83916    0.867    1.317    0.000   0.0372   0.06453;
  15     48.99    0.100   0.0657    19.96      0.0    8.605    22.39    74.45  4.24302    0.852    1.343    0.000   0.0402   0.06573;
  16     48.98    0.100   0.0669    19.96      0.0    9.083    22.25    73.02  4.63890    0.838    1.369    0.000   0.0433   0.06694;
  17     48.98    0.100   0.0682    19.97      0.0    9.552    22.11    71.62  5.02696    0.823    1.396    0.000   0.0464   0.06818;
  18     48.98    0.100   0.0694    19.97      0.0    10.01    21.97    70.24  5.40736    0.809    1.424    0.000   0.0496   0.06945;
  19     48.98    0.100   0.0707    19.97      0.0    10.46    21.83    68.89  5.78026    0.796    1.452    0.000   0.0528   0.07073;
  20     48.98    0.100    0.072    19.98      0.0    10.90    21.70    67.56  6.14580    0.782    1.480    0.000   0.0561   0.07204;
  21     48.98    0.100   0.0734    19.99      0.0    11.34    21.56    66.26  6.50415    0.769    1.509    0.000   0.0594   0.07336;
  22     48.98    0.100   0.0747    19.99      0.0    11.76    21.44    64.99  6.85543    0.756    1.539    0.000   0.0628   0.07471;
  23     48.98    0.100   0.0761    20.00      0.0    12.18    21.31    63.73  7.19981    0.743    1.569    0.000   0.0663   0.07609;
  24     48.97    0.100   0.0775    20.01      0.0    12.59    21.19    62.50  7.53740    0.731    1.600    0.000   0.0699   0.07749;
  25     48.97    0.100   0.0789    20.03      0.0    12.99    21.06    61.30  7.86836    0.719    1.631    0.000   0.0735   0.07891;
  26     48.97    0.100   0.0804    20.04      0.0    13.38    20.95    60.12  8.19282    0.707    1.663    0.000   0.0772   0.08035;
  27     48.97    0.100   0.0818    20.05      0.0    13.76    20.83    58.96  8.51090    0.695    1.696    0.000   0.0809   0.08182;
  28     48.97    0.100   0.0833    20.07      0.0    14.14    20.71    57.82  8.82273    0.683    1.730    0.000   0.0847   0.08332;
  29     48.97    0.100   0.0848    20.08      0.0    14.51    20.60    56.70  9.12844    0.672    1.764    0.000   0.0886   0.08484;
  30     48.97    0.100   0.0864    20.10      0.0    14.87    20.49    55.61  9.42815    0.661    1.798    0.000   0.0926   0.08638;
  31     48.96    0.100    0.088    20.12      0.0    15.23    20.39    54.53  9.72199    0.650    1.834    0.000   0.0967   0.08795;
  32     48.96    0.100   0.0895    20.14      0.0    15.58    20.28    53.48  10.0101    0.640    1.870    0.000    0.101   0.08955;
  33     48.96    0.100   0.0912    20.16      0.0    15.92    20.18    52.44  10.2925    0.629    1.907    0.000    0.105   0.09117;
  34     48.96    0.100   0.0928    20.19      0.0    16.25    20.07    51.43  10.5694    0.619    1.944    0.000    0.109   0.09282;
  35     48.96    0.100   0.0945    20.21      0.0    16.58    19.97    50.43  10.8408    0.609    1.983    0.000    0.114    0.0945;
  36     48.96    0.100   0.0962    20.24      0.0    16.90    19.88    49.46  11.1070    0.600    2.022    0.000    0.118    0.0962;
"""