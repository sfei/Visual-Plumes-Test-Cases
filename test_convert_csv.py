import os, math, csv


def csv_outputs(output_dict, folderpath, filename_format):
    case_digits = int(math.log10(output_dict['cases']))
    if case_digits < 2:
        case_digits = 2
    case_format = "{0:0" + str(case_digits) + "d}"
    if filename_format.lower().endswith(".csv"):
        filename_format = filename_format[:-4]

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)

    # print general params
    fp_memos = os.path.join(folderpath, f"{filename_format}.params.txt")
    with open(fp_memos, 'w') as fmemo:
        # print model param memos
        memos = output_dict['modelparams']['memos']
        if len(memos):
            fmemo.write("\n".join(memos) + "\n")

    diff_outs = output_dict['diffuser']
    amb_outs  = output_dict['ambient']
    um_outs   = output_dict['plume']
    ff_outs   = output_dict['farfield']
    tpb_outs  = output_dict['tpb']

    # prep headers for diffuser outputs
    diff_header_vals = ["Case"]
    for i, hdr in enumerate(diff_outs['headers']):
        header_text = hdr['label']
        if hdr['units_label'] != "":
            header_text += f" ({hdr['units_label']})"
        diff_header_vals.append(header_text)
    # prep headers for ambient outputs
    amb_header_vals = []
    for i, hdr in enumerate(amb_outs['headers']):
        header_text = hdr['label']
        if hdr['units_label'] != "":
            header_text += f" ({hdr['units_label']})"
        amb_header_vals.append(header_text)
    # prep headers for plume outputs
    header_vals = ["Step"]
    for i, hdr in enumerate(um_outs['headers']):
        header_text = hdr['label']
        if hdr['units_label'] != "":
            header_text += f" ({hdr['units_label']})"
        header_vals.append(header_text)
    # prep headers for brooks ff outputs
    ff_header_vals = []
    if ff_outs['was_run'] and len(ff_outs['headers']):
        for i, hdr in enumerate(ff_outs['headers']):
            header_text = hdr['label']
            if hdr['units_label'] != "":
                header_text += f" ({hdr['units_label']})"
            ff_header_vals.append(header_text)

    # diffuser csv
    fp_diff = os.path.join(folderpath, f"{filename_format}.diffuser.csv")
    with open(fp_diff, 'w', newline='') as fcsv:
        writer = csv.writer(fcsv)
        writer.writerow(diff_header_vals)
        for case_i, outputs in enumerate(diff_outs['outputs']):
            writer.writerow([case_i+1] + list(outputs))

    # loop by case
    for case_i in range(output_dict['cases']):
        case_n  = case_i+1
        case_fn = case_format.format(case_n)

        # ambient csv
        fp_amb = os.path.join(folderpath, f"{filename_format}.{case_fn}.ambient.csv")
        with open(fp_amb, 'w', newline='') as fcsv:
            writer = csv.writer(fcsv)
            writer.writerow(amb_header_vals)
            writer.writerows(amb_outs['outputs'][case_i])

        # print memos
        fp_memos = os.path.join(folderpath, f"{filename_format}.{case_fn}.memos.txt")
        with open(fp_memos, 'w') as fmemo:
            fmemo.write("---------------------------------------------------\n")
            fmemo.write(f"Case {case_n} (+{output_dict['casetime'][case_i]/3600.0:.2f} hrs):\n")
            fmemo.write("---------------------------------------------------\n")
            # print timeseries indices
            if output_dict['timeseries']:
                for memo in output_dict['timeseries']['memos'][case_i]:
                    fmemo.write(memo+"\n")
            # print model memos
            memos = um_outs['memos'][case_i]
            if len(memos):
                fmemo.write("\n" + "\n".join(memos) + "\n")
            # print post model memos
            memos = um_outs['postmemos'][case_i]
            if len(memos):
                fmemo.write("\n" + "\n".join(memos) + "\n")
            # print ff memos
            if ff_outs['was_run']:
                fmemo.write("\n" + "\n".join(ff_outs['memos'][case_i]) + "\n")

        # plume csv
        fp_plume = os.path.join(folderpath, f"{filename_format}.{case_fn}.plume.csv")
        with open(fp_plume, 'w', newline='') as fcsv:
            writer = csv.writer(fcsv)
            writer.writerow(header_vals)
            for output in um_outs['outputs'][case_i]:
                writer.writerow([output['step']] + output['values'] + [output['status']])

        # brooks ff csv
        if ff_outs['was_run']:
            fp_bff = os.path.join(folderpath, f"{filename_format}.{case_fn}.farfield.csv")
            with open(fp_bff, 'w', newline='') as fcsv:
                writer = csv.writer(fcsv)
                writer.writerow(ff_header_vals)
                for output in ff_outs['outputs'][case_i]:
                    writer.writerow(output['values'])

    # tidal pollution buildup outputs
    if tpb_outs['was_run']:
        fp_tpb = os.path.join(folderpath, f"{filename_format}.tpb.txt")
        with open(fp_tpb, 'w', newline='') as ftxt:
            ftxt.write("\n".join(tpb_outs['memos']))
