import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    anat_t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    func_rest_pre = create_key('sub-{subject}/func/sub-{subject}_task-rest_run-01_bold')

    info = {
        anat_t1w: [],
        func_rest_pre: []
    }

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """

        if ('mprage' in s.protocol_name) and (s.dim3 == 176):
            info[anat_t1w].append(s.series_id)

        if (s.protocol_name == 'restingstate') and (s.is_motion_corrected == False):
            info[func_rest_pre].append(s.series_id)

    return info
