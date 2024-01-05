from visualplumes import units, Middleware, OutputUM3, Ambient, AmbientStore, ModelParameters, BacteriaModel, \
                         SimilarityProfile, MaxVerticalReversals, DiffuserParameters, DiffuserStore
from test_print_outputs import print_outputs


# initialize all parameter handlers

model_params  = ModelParameters()
diff_params   = DiffuserParameters()
diff_store    = DiffuserStore()
ambient_store = AmbientStore()

# model_parameters (only changed from default)
model_params.current_vector_averaging   = True
model_params.write_step_freq            = 100
model_params.max_reversals              = MaxVerticalReversals.SECOND_MAX_RISE_OR_FALL
model_params.max_dilution               = 830
model_params.bacteria_model             = BacteriaModel.COLIFORM_MANCINI
model_params.at_equilibrium             = True
model_params.similarity_profile         = SimilarityProfile.DEFAULT
# model parameters (far-field model)
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
ambient_store.bg_conc.units       = units.Concentration.PARTS_PER_BILLION
ambient_store.decay_rate.units    = units.DecayRate.PER_SECOND
ambient_store.ff_diff_coeff.units = units.EddyDiffusivity.DIFFUSIVITY

ambient_stack = []

ambient_depth0 = Ambient()
ambient_depth0.z             = 0
ambient_depth0.current_speed = 0
ambient_depth0.current_dir   = 0
ambient_depth0.salinity      = 33.47
ambient_depth0.temperature   = 17
ambient_depth0.bg_conc       = 0
ambient_depth0.decay_rate    = 0.012
ambient_depth0.ff_velocity   = 0
ambient_depth0.ff_dir        = 0
ambient_depth0.ff_diff_coeff = 0
ambient_stack.append(ambient_depth0)

depths       = [3.0478, 6.0957, 9.1435, 12.1914, 15.2392, 18.2871, 21.3349, 24.3828, 27.4306, 30.4785, 33.5263, 36.5742,
                39.6221, 42.67]
salinities   = [33.462, 33.475, 33.477, 33.398, 33.156, 32.803, 32.68, 32.567, 32.545, 32.49, 32.483, 32.483, 32.5, 32.5]
temperatures = [16.993, 16.95, 16.812, 16.392, 14.809, 13.206, 12.409, 12.046, 11.88, 11.881, 11.79, 11.79, 11.777, 11.777]
for i, depth in enumerate(depths):
    ambient_depth_x = Ambient()
    ambient_depth_x.z             = depth
    ambient_depth_x.salinity      = salinities[i]
    ambient_depth_x.temperature   = temperatures[i]
    ambient_stack.append(ambient_depth_x)

ambient_stack[-5].decay_rate = 0.004

# Setup outputs handler
output_handler = OutputUM3()
# Add parameters to outputs: regime     parameter name    label        unit class           unit type
output_handler.add_parameter('element', 'depth',          'Depth',     units.Length,        diff_store.depth.units)
output_handler.add_parameter('element', 'diameter',       'Diameter',  units.Length,        diff_store.diameter.units)
output_handler.add_parameter('element', 'vertical_angle', 'V-angle',   units.Angle,         units.Angle.DEGREES)
output_handler.add_parameter('element', 'salinity',       'Salinity',  units.Salinity,      ambient_store.salinity.units)
output_handler.add_parameter('element', 'temperature',    'Temp.',     units.Temperature,   ambient_store.temperature.units)
output_handler.add_parameter('ambient', 'kt',             'Decay',     units.DecayRate,     units.DecayRate.PER_SECOND)
output_handler.add_parameter('element', 'concentration',  'Pollutant', units.Concentration, diff_store.concentration.units)
output_handler.add_parameter('element', 'density',        'Density',   units.Density,       units.Density.SIGMA_T)
output_handler.add_parameter('ambient', 'density',        'Amb-den',   units.Density,       units.Density.SIGMA_T)
output_handler.add_parameter('element', 'dilution',       'Dilution',  units.Unitless,      units.Unitless.UNITLESS)
output_handler.add_parameter('element', 'speed',          'Velocity',  units.Speed,         ambient_store.current_speed.units)
output_handler.add_parameter('element', 'x_displacement', 'X-pos',     units.Length,        units.Length.FEET)

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

Simulation:
Froude No:     22.07; Strat No: 1.61E-5; Spcg No:   36.00; k: 2.51E+5; eff den (sigmaT) -1.267032; eff vel     2.513(m/s);
Current is very small, flow regime may be transient.

        Depth    Decay    P-dia Ver angl  Eff-sal     Temp  Polutnt  Density  P-speed   Dilutn   x-posn   y-posn   Iso dia
Step     (ft)    (s-1)     (in)    (deg)    (psu)      (C)    (ppb) (sigmaT)    (m/s)       ()     (ft)     (ft)       (m)
   0     140.0    0.004    2.000      0.0    1.340    22.50   1200.0 -1.26703    2.513    1.000      0.0      0.0    0.0508;
   1     140.0    0.004    2.058   0.0174    3.129    21.88   1132.8  0.22983    2.369    1.059   0.0233      0.0   0.05229; bottom hit;
 100     139.9    0.004    14.68    7.819    28.36    13.20    162.2  21.2507    0.337    7.358    2.637      0.0    0.3728;
 200     138.3    0.004    32.47    36.35    30.80    12.36    65.10  23.2922    0.170    17.90    6.537      0.0    0.8247;
 300     132.8    0.004    52.27    64.64    31.73    12.04    27.94  24.0701    0.145    39.46    10.64      0.0    1.3276;
 337     125.8    0.004    72.25    74.92    32.07    11.93    14.75  24.3510    0.134    70.05    13.08      0.0    1.8352; merging;
 400     76.16   0.0058    177.2    86.09    32.38    11.88    2.630  24.6045    0.148    243.4    19.29      0.0    4.5011;
 417     48.05    0.008    251.2    87.01    32.50    12.20    1.253  24.6326    0.138    340.8    20.89      0.0    6.3805; trap level;
 431     31.00   0.0095    693.2    83.17    32.59    12.63    0.684  24.6262    0.053    388.1    22.04      0.0    17.607; begin overlap;
 458     29.23  0.00966   1614.2    74.95    32.60    12.64    0.595  24.6260   0.0243    388.7    22.34      0.0    41.002; ceiling;
 473     29.05  0.00968   2095.5    70.50    32.60    12.64    0.579  24.6260   0.0189    388.7    22.39      0.0    53.226; surface;
 
Horiz plane projections in effluent direction: radius(m):      0.0; CL(m):   6.8251
Lmz(m):   6.8251
forced entrain      1     0.0   33.82   53.23   0.329
Rate sec-1    0.0096751 dy-1      835.930  kt:    0.0096751 Amb Sal      33.4768
Highest buildup of concentration:          0.0

"""