from test_convert_csv import csv_outputs
from visualplumes import units, Middleware, OutputUM3, Ambient, AmbientStore, ModelParameters, BacteriaModel, \
                         SimilarityProfile, FarfieldDiffusivity, MaxVerticalReversals, DiffuserParameters, \
                         DiffuserStore, AmbientTimeseries, DiffuserTimeseries, TimeseriesHandler
from test_print_outputs import print_outputs
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt


# initialize all parameter handlers
model_params  = ModelParameters()
diff_params   = DiffuserParameters()
diff_store    = DiffuserStore()
ambient_store = AmbientStore()
timeseries    = TimeseriesHandler()

# model parameters
model_params.current_vector_averaging = True
model_params.contraction_coeff        = 1.0
model_params.light_absorb_coeff       = 1.6
model_params.aspiration_coeff         = 0.1
model_params.bacteria_model           = BacteriaModel.COLIFORM_MANCINI
model_params.at_equilibrium           = True
model_params.similarity_profile       = SimilarityProfile.DEFAULT
model_params.farfield_diffusivity     = FarfieldDiffusivity.POWER_4_3
# tidal pollution buildup parameters
model_params.tidal_pollution_buildup  = True
model_params.tpb_channel_width        = 39.6  # all units assumed meters or degrees
model_params.tpb_segment_length       = 80.46
model_params.tpb_upstream_dir         = 180
model_params.tpb_coast_bin            = 65
model_params.tpb_coast_concentration  = 9e-6
model_params.tpb_mixing_zone_ceil     = 3.657
# output and plume stop conditions and miscse
model_params.output_all_ff_increments = False
model_params.stop_on_bottom_hit       = False
model_params.dont_stop_on_surface_hit = False
model_params.allow_induced_current    = False

# the start time, end time, and time increment from the diffuser table are handled in timeseries handler
timeseries.start_time           = 0
timeseries.end_time             = 143  #143
timeseries.time_increment       = 1
timeseries.units.start_time     = units.Time.HOURS
timeseries.units.end_time       = units.Time.HOURS
timeseries.units.time_increment = units.Time.HOURS

# diffuser parameters
diff_params.diameter                 = 0.0254
diff_store.diameter.units            = units.Length.METERS
diff_params.offset_x                 = 0.0
# diff_store.offset_x.units            = units.Length.FEET
diff_params.offset_y                 = 0.0
# diff_store.offset_y.units            = units.Length.FEET
diff_params.vertical_angle           = 22.5
diff_store.vertical_angle.units      = units.Angle.DEGREES
diff_params.horizontal_angle         = 270.0
diff_store.horizontal_angle.units    = units.Angle.DEGREES
diff_params.num_ports                = 1
diff_store.num_ports.units           = units.Unitless.UNITLESS
diff_params.acute_mixing_zone        = 30
diff_store.acute_mixing_zone.units   = units.Length.FEET
diff_params.isopleth                 = 60.0
diff_store.isopleth.units            = units.Isopleth.CONCENTRATION
diff_params.depth                    = 5.0
diff_store.depth.units               = units.Length.FEET
diff_params.salinity                 = 15.0
diff_store.salinity.units            = units.Salinity.PRACTICAL_SALINITY_UNITS
diff_params.temperature              = 25.0
diff_store.temperature.units         = units.Temperature.CELSIUS
diff_params.concentration            = 8300.0
diff_store.concentration.units       = units.Concentration.PARTS_PER_MILLION

# Setup diffuser timeseries (directly set in handler per variable)
#diff_store.effluent_flow.from_time_series = True  # can set this but also done via handler in middleware)
diff_store.effluent_flow.units            = units.FlowRate.MEGAGALLONS_PER_DAY  # uses same store value, but units for value
diff_store.effluent_flow.ts_increment     = 1.0                                 # this is assumed as hours (no UI for time units)
timeseries.diffuser.effluent_flow         = DiffuserTimeseries("./TRwtp_tsfiles/flowrate.csv", diff_store.effluent_flow)

# Setup ambient conditions
# All other ambient store parameters left at defaults, which are:
#    z_is_depth = True
#    extrapolation_sfc = Interpolation.CONSTANT
#    extrapolation_btm = Interpolation.CONSTANT
#    no time-series data
ambient_store.z.units             = units.Length.FEET
ambient_store.salinity.units      = units.Salinity.PRACTICAL_SALINITY_UNITS
ambient_store.temperature.units   = units.Temperature.CELSIUS
ambient_store.bg_conc.units       = units.Concentration.PARTS_PER_MILLION
ambient_store.ff_diff_coeff.units = units.EddyDiffusivity.DIFFUSIVITY
# Two depth layers at 0 and 50m, with only surface conditions defined
# (with constant extrapolation to bottom, basically assumes constant conditions to depth)
ambient_depth0 = Ambient()
ambient_depth0.z             = 0
ambient_depth0.current_speed = 0  # to be overwritten from timeseries
ambient_depth0.current_dir   = 0  # to be overwritten from timeseries
ambient_depth0.salinity      = 0.2
ambient_depth0.temperature   = 25
ambient_depth0.bg_conc       = 9
ambient_depth0.decay_rate    = 0
ambient_depth0.ff_diff_coeff = 0.0003
# Note that default values are None in Ambient class. This means values will be interpolated / extrapolated.
ambient_depth12 = Ambient()
ambient_depth12.z            = 12
ambient_depth12.temperature  = 22.2

ambient_stack = (ambient_depth0, ambient_depth12)

# Setup ambient timeseries (directly set in handler per variable)
ambient_store.current_dir.z_is_depth         = True                 # timeseries may be depth/height layers indepedently
ambient_store.current_dir.ts_depth_units     = units.Length.FEET    # depth units
ambient_store.current_dir.units              = units.Angle.DEGREES  # uses same store value, but units for value
ambient_store.current_dir.ts_increment       = 1.0                  # this is assumed as hours (no UI for time units)
timeseries.ambient.current_dir               = AmbientTimeseries("./TRwtp_tsfiles/current_dir.csv", ambient_store.current_dir)
ambient_store.current_speed.z_is_depth       = True
ambient_store.current_speed.ts_depth_units   = units.Length.FEET
ambient_store.current_speed.units            = units.Speed.FEET_PER_SECOND
ambient_store.current_speed.ts_increment     = 1.0
timeseries.ambient.current_speed             = AmbientTimeseries("./TRwtp_tsfiles/current_speed.csv", ambient_store.current_speed)

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
output_handler.add_parameter('ambient', 'density',        'Amb-den',   units.Density,       units.Density.SIGMA_T)
output_handler.add_parameter('ambient', 'current_speed',  'Amb-cur',   units.Speed,         ambient_store.current_speed.units)
output_handler.add_parameter('element', 'speed',          'Velocity',  units.Speed,         units.Speed.METERS_PER_SECOND)
output_handler.add_parameter('element', 'dilution',       'Dilution',  units.Unitless,      units.Unitless.UNITLESS)
output_handler.add_parameter('element', 'x_displacement', 'X-pos',     units.Length,        units.Length.FEET)
output_handler.add_parameter('element', 'y_displacement', 'Y-pos',     units.Length,        units.Length.FEET)
# output_handler.add_parameter('element', 'mass',           'Mass',      units.Mass,          units.Mass.KILOGRAMS)
# output_handler.add_parameter('element', 'd_mass',         'Entrained', units.Mass,          units.Mass.KILOGRAMS)
output_handler.add_parameter('model',    'iso_diameter',  'Iso diameter', units.Length,     diff_store.diameter.units)

start_dt = datetime.now()
# run model
output_dict = Middleware.run(
    model_params=model_params,
    diffuser_params=diff_params,
    diffuser_store=diff_store,
    timeseries_handler=timeseries,
    ambient_stack=ambient_stack,
    ambient_store=ambient_store,
    output_handler=output_handler
)
end_dt = datetime.now()

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
    # plot('trajectory', 'boundary1', 'boundary2', flip_y=True)
    print_outputs(output_dict)
    # csv_outputs(output_dict, "./outcsvs", "TRwtp")
elif output_dict["error"]:
    print(output_dict["error"])
else:
    print("Unknown error")

print("")
print("Start time: "+start_dt.strftime("%Y-%m-%d %H:%M:%S"))
print("End time:   "+end_dt.strftime("%Y-%m-%d %H:%M:%S"))

