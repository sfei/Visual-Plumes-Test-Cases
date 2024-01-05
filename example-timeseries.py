from visualplumes import units, Middleware, OutputUM3, Ambient, AmbientStore, ModelParameters, BacteriaModel, \
                         SimilarityProfile, MaxVerticalReversals, DiffuserParameters, DiffuserStore, \
                         AmbientTimeseries, DiffuserTimeseries, TimeseriesHandler
from test_print_outputs import print_outputs


# initialize all parameter handlers
model_params  = ModelParameters()
diff_params   = DiffuserParameters()
diff_store    = DiffuserStore()
ambient_store = AmbientStore()
timeseries    = TimeseriesHandler()

# all model parameters left at defaults for now.. (should set brooks far field, but that part isn't written yet)
# whoops, even without tidal pollution buildup enabled, there's a parameter that factors into calculation of the stream
# limit stop condition (TODO: why? if not TPB, shouldn't this condition be disabled?)
model_params.tpb_channel_width       = 100  # all units assumed meters or degrees
model_params.tpb_segment_length      = 50
model_params.tpb_upstream_dir        = 0
model_params.tpb_coast_bin           = 0
model_params.tpb_coast_concentration = 0
model_params.tpb_mixing_zone_ceil    = 0

# the start time, end time, and time increment from the diffuser table are handled in timeseries handler
timeseries.start_time           = 0
timeseries.end_time             = 12
timeseries.time_increment       = 1
timeseries.units.start_time     = units.Time.HOURS
timeseries.units.end_time       = units.Time.HOURS
timeseries.units.time_increment = units.Time.HOURS

# diffuser parameters
diff_params.diameter                 = 0.05
diff_store.diameter.units            = units.Length.METERS
diff_params.offset_x                 = 0.0
diff_store.offset_x.units            = units.Length.METERS
diff_params.offset_y                 = 0.0
diff_store.offset_y.units            = units.Length.METERS
diff_params.vertical_angle           = 20
diff_store.vertical_angle.units      = units.Angle.DEGREES
diff_params.horizontal_angle         = 90
diff_store.horizontal_angle.units    = units.Angle.N_DEGREES
diff_params.num_ports                = 1
diff_store.num_ports.units           = units.Unitless.UNITLESS
diff_params.acute_mixing_zone        = 10
diff_store.acute_mixing_zone.units   = units.Length.METERS
diff_params.isopleth                 = 0
diff_store.isopleth.units            = units.Isopleth.CONCENTRATION
diff_params.depth                    = 49
diff_store.depth.units               = units.Length.METERS
diff_params.salinity                 = 0
diff_store.salinity.units            = units.Salinity.PRACTICAL_SALINITY_UNITS
diff_params.temperature              = 25
diff_store.temperature.units         = units.Temperature.CELSIUS
diff_params.concentration            = 100
diff_store.concentration.units       = units.Concentration.PARTS_PER_MILLION

# Setup diffuser timeseries (directly set in handler per variable)
#diff_store.effluent_flow.from_time_series = True  # can set this but also done via handler in middleware)
diff_store.effluent_flow.units            = units.FlowRate.MEGAGALLONS_PER_DAY  # uses same store value, but units for value
diff_store.effluent_flow.ts_increment     = 1.0                                 # this is assumed as hours (no UI for time units)
timeseries.diffuser.effluent_flow         = DiffuserTimeseries("./ts_example/ts_eff_flow.csv", diff_store.effluent_flow)

# Setup ambient conditions
# All other ambient store parameters left at defaults, which are:
#    z_is_depth = True
#    extrapolation_sfc = Interpolation.CONSTANT
#    extrapolation_btm = Interpolation.CONSTANT
#    no time-series data
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
ambient_depth0.current_speed = None  # to be from timeseries
ambient_depth0.current_dir   = None  # to be from timeseries
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

ambient_stack = (ambient_depth0, ambient_depth50)

# Setup ambient timeseries (directly set in handler per variable)
#ambient_store.current_dir.from_time_series   = True  # can set this but also done via handler in middleware)
ambient_store.current_dir.z_is_depth         = True                 # timeseries may be depth/height layers indepedently
ambient_store.current_dir.ts_depth_units     = units.Length.METERS  # depth units
ambient_store.current_dir.units              = units.Angle.DEGREES  # uses same store value, but units for value
ambient_store.current_dir.ts_increment       = 1.0                  # this is assumed as hours (no UI for time units)
timeseries.ambient.current_dir               = AmbientTimeseries("./ts_example/ts_current_dir.csv", ambient_store.current_dir)
#ambient_store.current_speed.from_time_series = True  # can set this but also done via handler in middleware)
ambient_store.current_speed.z_is_depth       = True
ambient_store.current_speed.ts_depth_units   = units.Length.METERS
ambient_store.current_speed.units            = units.Speed.METERS_PER_SECOND
ambient_store.current_speed.ts_increment     = 1.0
timeseries.ambient.current_speed             = AmbientTimeseries("./ts_example/ts_current_spd.csv", ambient_store.current_speed)

# Setup outputs handler
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
    timeseries_handler=timeseries,
    ambient_stack=ambient_stack,
    ambient_store=ambient_store,
    output_handler=output_handler
)

print_outputs(output_dict)
