from visualplumes import units


def print_outputs(output_dict):
    # prep diffuser output formatting (since same for all cases)
    diff_outs = output_dict['diffuser']
    header_vals = []
    units_vals = []
    format_header = []
    format_output = []
    for i, hdr in enumerate(diff_outs['headers']):
        header_vals.append(hdr['label'])
        hdr_len = len(hdr['label']) + (1 if i > 0 else 0)
        hdr_units = hdr['units']
        format_header.append("{" + str(i) + ":>" + str(hdr_len) + "}")
        if i == 0 or hdr_units == units.FlowRate:
            format_output.append("{" + str(i) + ":" + str(hdr_len) + ".5f}")
        else:
            format_output.append("{" + str(i) + ":" + str(hdr_len) + ".1f}")
        if hdr['units_label'] == "":
            units_vals.append("")
        else:
            units_vals.append(f"({hdr['units_label']})")
    diff_format_header = " ".join(format_header)
    diff_format_output = " ".join(format_output)
    diff_str_header = diff_format_header.format(*header_vals)
    diff_str_units = diff_format_header.format(*units_vals)

    # prep ambient output formatting (since same for all cases)
    ambient_outs = output_dict['ambient']
    header_vals = []
    units_vals = []
    format_header = []
    format_output = []
    for i, hdr in enumerate(ambient_outs['headers']):
        header_vals.append(hdr['label'])
        hdr_len = len(hdr['label']) + (1 if i > 0 else 0)
        if hdr_len < 7:
            hdr_len = 7
        if hdr['units_label'] == "":
            units_vals.append("")
        else:
            units_vals.append(f"({hdr['units_label']})")
        if hdr['label'].startswith("Far-field"):
            continue
        if hdr['units'] == units.Angle:
            val_precision = 0
        elif hdr['units'] == units.Length:
            val_precision = 3
        elif hdr['units'] in (units.Speed, units.Density, units.DecayRate):
            val_precision = 4
        elif hdr['units'] in (units.Concentration, units.Salinity, units.Temperature):
            val_precision = 2
        else:
            val_precision = 1
        format_header.append("{" + str(i) + ":>" + str(hdr_len) + "}")
        format_output.append("{" + str(i) + ":" + str(hdr_len) + "." + str(val_precision) + "f}")
    amb_format_header = " ".join(format_header)
    amb_format_output = " ".join(format_output)
    amb_str_header = amb_format_header.format(*header_vals)
    amb_str_units = amb_format_header.format(*units_vals)

    # prep model output formatting (since same for all cases)
    model_outs = output_dict['plume']
    format_header = ["{0:>5}"]
    format_output = ["{0:5}"]
    header_vals = ["Step"]
    units_vals = [""]
    # output_handler.headers() returns a generation/yield, so if you want to package it, wrap it in a list() or tuple()
    for i, hdr in enumerate(model_outs['headers']):
        header_vals.append(hdr['label'])
        if hdr['units_label'] == "":
            units_vals.append("")
        else:
            units_vals.append("(" + hdr['units_label'] + ")")
        # if hdr['units'] == units.DecayRate:
        #     format_header.append("{" + str(i + 1) + ":>10}")
        #     format_output.append("{" + str(i + 1) + ":10.1f}")
        if hdr['units'] == units.Angle:
            format_header.append("{" + str(i + 1) + ":>8}")
            format_output.append("{" + str(i + 1) + ":8.3f}")
        elif hdr['name'] == 'd_mass':
            format_header.append("{" + str(i + 1) + ":>9}")
            format_output.append("{" + str(i + 1) + ":9.5f}")
        elif hdr['units'] == units.Density:
            format_header.append("{" + str(i + 1) + ":>9}")
            format_output.append("{" + str(i + 1) + ":9.4f}")
        elif hdr['units'] in (units.Concentration, units.Speed):
            format_header.append("{" + str(i + 1) + ":>9}")
            format_output.append("{" + str(i + 1) + ":9.3f}")
        elif hdr['name'] == 'dilution':
            format_header.append("{" + str(i + 1) + ":>9}")
            format_output.append("{" + str(i + 1) + ":9,.3f}")
        elif hdr['name'] == 'diameter' or hdr['units'] == units.DecayRate:
            format_header.append("{" + str(i + 1) + ":>9}")
            format_output.append("{" + str(i + 1) + ":9,.4f}")
        elif hdr['name'] in ('depth', 'iso_diameter', 'x_displacement', 'y_displacement'):
            format_header.append("{" + str(i + 1) + ":>9}")
            format_output.append("{" + str(i + 1) + ":9,.3f}")
        else:
            format_header.append("{" + str(i + 1) + ":>9}")
            format_output.append("{" + str(i + 1) + ":9.2f}")
    model_format_header = " ".join(format_header)
    model_format_output = " ".join(format_output)
    model_str_header = model_format_header.format(*header_vals)
    model_str_units = model_format_header.format(*units_vals)

    # prep brooks far-field model formatting (since same for all cases)
    ff_outs = output_dict['farfield']
    format_header = []
    format_output = []
    header_vals = []
    units_vals = []
    if ff_outs['was_run'] and len(ff_outs['headers']):
        for i, hdr in enumerate(ff_outs['headers']):
            header_vals.append(hdr['label'])
            if hdr['units_label'] == "":
                units_vals.append("")
            else:
                units_vals.append(f"({hdr['units_label']})")
            hdr_len = len(hdr['label']) + (1 if i > 0 else 0)
            if hdr_len < 6:
                hdr_len = 6
            val_precision = 1
            match hdr['name']:
                case 'dilution':
                    val_precision = 1
                    if hdr_len < 9:
                        hdr_len = 9
                case 'adj_width':
                    val_precision = 0
                    if hdr_len < 8:
                        hdr_len = 8
                case 'total_surf_dsp':
                    val_precision = 1
                    if hdr_len < 9:
                        hdr_len = 9
                case 'ff_diff_coeff':
                    val_precision = 4
                    if hdr_len < 12:
                        hdr_len = 12
                case 'diffusivity':
                    val_precision = 4
                    if hdr_len < 9:
                        hdr_len = 9
                case _:
                    if hdr['units'] in (units.Speed, units.Time):
                        val_precision = 2
                        if hdr_len < 8:
                            hdr_len = 8
                    elif hdr['units'] == units.Concentration:
                        val_precision = 4
            format_header.append("{" + str(i) + ":>" + str(hdr_len) + "}")
            format_output.append("{" + str(i) + ":" + str(hdr_len) + ",." + str(val_precision) + "f}")
        ff_format_header = " ".join(format_header)
        ff_format_output = " ".join(format_output)
        ff_str_header = ff_format_header.format(*header_vals)
        ff_str_units = ff_format_header.format(*units_vals)
    else:
        ff_format_header = ""
        ff_format_output = ""
        ff_str_header = ""
        ff_str_units = ""

    # print model parameters header
    if 'modelparams' in output_dict:
        for memo in output_dict['modelparams']['memos']:
            print(memo)
        print("")

    # loop outputs by case run
    for case_i in range(output_dict['cases']):
        print("\n---------------------------------------------------")
        print(f"Case {1 + case_i} (+{output_dict['casetime'][case_i]/3600.0:.2f} hrs):")
        print("---------------------------------------------------")

        # print timeseries indices
        if output_dict['timeseries']:
            for memo in output_dict['timeseries']['memos'][case_i]:
                print(memo)

        # print diffuser params
        print("")
        print(diff_str_header)
        print(diff_str_units)
        print(diff_format_output.format(*diff_outs['outputs'][case_i]))

        # print ambient params
        print("")
        print(amb_str_header)
        print(amb_str_units)
        for amb_level in ambient_outs['outputs'][case_i]:
            print(amb_format_output.format(*amb_level))

        # print memos
        memos = model_outs['memos'][case_i]
        if len(memos):
            print("\n" + "\n".join(memos))

        # print output table
        print("")
        print(model_str_header)
        print(model_str_units)
        for output in model_outs['outputs'][case_i]:
            print(model_format_output.format(*([output['step']] + output['values'])) + f";  {output['status']}")

        # print post memos
        memos = model_outs['postmemos'][case_i]
        if len(memos):
            print("\n" + "\n".join(memos))

        # print ff output table
        if ff_outs['was_run']:
            print("")
            for memo in ff_outs['memos'][case_i]:
                print(memo)
            print("")
            if ff_str_header:
                print(ff_str_header)
                print(ff_str_units)
            for output in ff_outs['outputs'][case_i]:
                if len(output):
                    print(ff_format_output.format(*output['values']))

    # print ff output table
    if output_dict['tpb']['was_run']:
        print("")
        print("---------------------------------------------------")
        print("")
        for memo in output_dict['tpb']['memos']:
            print(memo)
