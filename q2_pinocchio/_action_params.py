# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from q2_types.feature_data import FeatureData, Sequence, Taxonomy
from q2_types.per_sample_sequences import (
    PairedEndSequencesWithQuality,
    SequencesWithQuality,
)
from q2_types.sample_data import SampleData
from qiime2.plugin import Bool, Choices, Float, Int, Range, Str, TypeMatch

from q2_pinocchio.types._type import Minimap2IndexDB, PairwiseAlignmentMN2

T = TypeMatch([SequencesWithQuality, PairedEndSequencesWithQuality])

# filter_reads
filter_reads_inputs = {
    "query_reads": SampleData[T],
    "index_database": Minimap2IndexDB,
    "reference_reads": FeatureData[Sequence],
}
filter_reads_outputs = [("filtered_query_reads", SampleData[T])]
filter_reads_inputs_dsc = {
    "query_reads": "Reads to be filtered.",
    "index_database": "Minimap2 index database. Incompatible with reference-reads.",
    "reference_reads": "Reference sequences. Incompatible with index-database.",
}
filter_reads_outputs_dsc = {
    "filtered_query_reads": "The resulting filtered sequences.",
}
filter_reads_params = {
    "n_threads": Int % Range(1, None),
    "mapping_preset": Str % Choices(["map-ont", "map-hifi", "map-pb", "sr"]),
    "keep": Str % Choices(["mapped", "unmapped"]),
    "min_per_identity": Float % Range(0.0, 1.0, inclusive_end=True),
    "matching_score": Int,
    "mismatching_penalty": Int,
    "gap_open_penalty": Int % Range(1, None),
    "gap_extension_penalty": Int % Range(1, None),
}
filter_reads_param_dsc = {
    "n_threads": "Number of threads to use.",
    "mapping_preset": "Specifies the type of input sequences that will be "
    "used during the mapping process. 1) map-ont: Align noisy long reads "
    "of ~10% error rate to a reference genome. 2) map-hifi: Align PacBio "
    "high-fidelity (HiFi) reads to a reference genome. 3) map-pb: Align "
    "older PacBio continuous long (CLR) reads to a reference genome. "
    "4) sr: Align short single-end reads.",
    "keep": "Keep the sequences that align to reference. When "
    "set to unmapped it keeps sequences that do not align to the reference "
    "database.",
    "min_per_identity": "After the alignment step, mapped reads will be "
    "reclassified as unmapped if their identity percentage falls below this "
    "value. If not set there is no reclassification.",
    "matching_score": "Matching score.",
    "mismatching_penalty": "Mismatching penalty.",
    "gap_open_penalty": "Gap open penalty.",
    "gap_extension_penalty": "Gap extension penalty.",
}
filter_reads_dsc = (
    "Filter demultiplexed single-end sequences based on "
    "alignment to a reference database using Minimap2 and samtools. "
    "This versatile command allows for the exclusion of long sequences "
    "or, when exclude_mapped is set to False, selectively retains only "
    "those sequences aligning to the reference."
)

# extract-seqs
extract_seqs_inputs = {
    "sequences": FeatureData[Sequence],
    "index_database": Minimap2IndexDB,
    "reference_reads": FeatureData[Sequence],
}
extract_seqs_inputs_dsc = {
    "sequences": "Feature sequences to be filtered.",
    "index_database": "Minimap2 index database. Incompatible with reference-reads.",
    "reference_reads": "Reference sequences. Incompatible with index-database.",
}
extract_seqs_outputs = [("extracted_seqs", FeatureData[Sequence])]
extract_seqs_outputs_dsc = {
    "extracted_seqs": "Subset of initial feature sequences that we keep.",
}
extract_seqs_params = {
    "n_threads": Int % Range(1, None),
    "mapping_preset": Str % Choices(["map-ont", "map-hifi", "map-pb", "sr"]),
    "extract": Str % Choices(["mapped", "unmapped"]),
    "min_per_identity": Float % Range(0.0, 1.0, inclusive_end=True),
    "matching_score": Int,
    "mismatching_penalty": Int,
    "gap_open_penalty": Int % Range(1, None),
    "gap_extension_penalty": Int % Range(1, None),
}
extract_seqs_param_dsc = {
    "n_threads": "Number of threads to use.",
    "mapping_preset": "Specifies the type of input sequences that will be "
    "used during the mapping process. 1) map-ont: Align noisy long reads "
    "of ~10% error rate to a reference genome. 2) map-hifi: Align PacBio "
    "high-fidelity (HiFi) reads to a reference genome. 3) map-pb: Align "
    "older PacBio continuous long (CLR) reads to a reference genome."
    "4) sr: Align short single-end reads.",
    "extract": "Extract sequences that map to reference. When "
    "set to unmapped it extracts sequences that do not map to the reference "
    "database.",
    "min_per_identity": "After the alignment step, mapped reads will be "
    "reclassified as unmapped if their identity percentage falls below this "
    "value. If not set there is no reclassification.",
    "matching_score": "Matching score.",
    "mismatching_penalty": "Mismatching penalty.",
    "gap_open_penalty": "Gap open penalty.",
    "gap_extension_penalty": "Gap extension penalty.",
}
extract_seqs_dsc = (
    "This method aligns feature sequences to a set of reference sequences to "
    "identify sequences that hit/miss the reference within a specified "
    "perc_identity. This method could be used to define a positive filter "
    "or a negative filter."
)

# build-index
build_index_inputs = {"sequences": FeatureData[Sequence]}
build_index_outputs = [("index_database", Minimap2IndexDB)]
build_index_inputs_dsc = {
    "sequences": "Reference sequences used to build Minimap2 index database."
}
build_index_outputs_dsc = {"index_database": "Minimap2 index database."}
build_index_params = {
    "preset": Str % Choices(["map-ont", "map-hifi", "map-pb", "sr"]),
}
build_index_param_dsc = {
    "preset": "This option applies multiple settings at the same time during "
    "the indexing process. This value should match the mapping preset value "
    "that is intended to be used in other actions utilizing the created index. "
    "The available presets are: "
    "1) map-ont: Align noisy long reads of ~10% error rate to a reference genome. "
    "2) map-hifi: Align PacBio high-fidelity (HiFi) reads to a reference genome. "
    "3) map-pb: Align older PacBio continuous long (CLR) reads to a reference genome. "
    "4) sr: Align short single-end reads.",
}
build_index_dsc = "Build Minimap2 index database from reference sequences."


# minimap2-search
minimap2_search_inputs = {
    "query_reads": FeatureData[Sequence],
    "index_database": Minimap2IndexDB,
    "reference_reads": FeatureData[Sequence],
}
minimap2_search_outputs = [("search_results", FeatureData[PairwiseAlignmentMN2])]
minimap2_search_inputs_dsc = {
    "query_reads": "Query reads.",
    "index_database": "Minimap2 index database. Incompatible with reference-reads.",
    "reference_reads": "Reference sequences. Incompatible with index-database.",
}
minimap2_search_outputs_dsc = {
    "search_results": "Top hits for each query.",
}
minimap2_search_param_dsc = {
    "n_threads": "Number of threads to use.",
    "maxaccepts": "Maximum number of hits to keep for each query. Minimap2 will "
    "choose the first N hits in the reference database.",
    "mapping_preset": "Specifies the type of input sequences that will be "
    "used during the mapping process. 1) map-ont: Align noisy long reads "
    "of ~10% error rate to a reference genome. 2) map-hifi: Align PacBio "
    "high-fidelity (HiFi) reads to a reference genome. 3) map-pb: Align "
    "older PacBio continuous long (CLR) reads to a reference genome."
    "4) sr: Align short single-end reads.",
    "perc_identity": "Optionally reject match if percent identity to query is "
    "lower.",
    "output_no_hits": "Report both matching and non-matching queries. "
    "WARNING: always use the default setting for this "
    "option unless if you know what you are doing! If "
    "you set this option to False, your sequences and "
    "feature table will need to be filtered to exclude "
    "unclassified sequences, otherwise you may run into "
    "errors downstream from missing feature IDs. Set to "
    "True to mirror default Minimap2 search.",
}
minimap2_search_params = {
    "n_threads": Int % Range(1, None),
    "maxaccepts": Int % Range(1, None),
    "mapping_preset": Str % Choices(["map-ont", "map-hifi", "map-pb", "sr"]),
    "perc_identity": Float % Range(0.0, 1.0, inclusive_end=True),
    "output_no_hits": Bool,
}
minimap2_search_dsc = (
    "Search for top hits in a reference database using alignment between the "
    "query sequences and reference database sequences using Minimap2. Returns a "
    "report of the top M hits for each query (where M=maxaccepts)."
)

# classify-consensus-minimap2
classify_consensus_minimap2_inputs = {
    "query": FeatureData[Sequence],
    "index_database": Minimap2IndexDB,
    "reference_reads": FeatureData[Sequence],
    "reference_taxonomy": FeatureData[Taxonomy],
}
classify_consensus_minimap2_outputs = [
    ("search_results", FeatureData[PairwiseAlignmentMN2]),
    ("classification", FeatureData[Taxonomy]),
]
classify_consensus_minimap2_inputs_dsc = {
    "query": "Query sequences.",
    "index_database": "Minimap2 indexed database. "
    "Incompatible with reference-reads.",
    "reference_reads": "Reference sequences. Incompatible with index-database.",
    "reference_taxonomy": "Reference taxonomy labels.",
}

classify_consensus_minimap2_outputs_dsc = {
    "search_results": "Top hits for each query.",
    "classification": "Taxonomy classifications of query sequences.",
}
classify_consensus_minimap2_params = {
    "maxaccepts": Int % Range(1, None),
    "mapping_preset": Str % Choices(["map-ont", "map-hifi", "map-pb", "sr"]),
    "perc_identity": Float % Range(0.0, 1.0, inclusive_end=True),
    "output_no_hits": Bool,
    "num_threads": Int % Range(1, None),
    "min_consensus": Float % Range(0.5, 1.0, inclusive_end=True, inclusive_start=False),
    "unassignable_label": Str,
}
classify_consensus_minimap2_param_dsc = {
    "maxaccepts": (
        "Maximum number of hits to keep for each query. Minimap2 will "
        "choose the first N hits in the reference database that "
        "exceed perc_identity similarity to query."
    ),
    "mapping_preset": "Specifies the type of input sequences that will be "
    "used during the mapping process. 1) map-ont: Align noisy long reads "
    "of ~10% error rate to a reference genome. 2) map-hifi: Align PacBio "
    "high-fidelity (HiFi) reads to a reference genome. 3) map-pb: Align "
    "older PacBio continuous long (CLR) reads to a reference genome."
    "4) sr: Align short single-end reads.",
    "perc_identity": ("Reject match if percent identity to query is lower."),
    "output_no_hits": "Report both matching and non-matching queries. ",
    "num_threads": "Number of threads (CPUs) to use in the Minimap2 search. "
    "Pass 0 to use all available CPUs.",
    "min_consensus": "Minimum fraction of assignments must match top "
    "hit to be accepted as consensus assignment.",
    "unassignable_label": "Annotation given to sequences without any hits.",
}
classify_consensus_minimap2_dsc = (
    "Assign taxonomy to query sequences using Minimap2. Performs "
    "alignment between query and reference_reads, then "
    "assigns consensus taxonomy to each query sequence from "
    "among maxaccepts hits, min_consensus of which share "
    "that taxonomic assignment."
)

# find-consensus-annotation
find_consensus_annotation_inputs = {
    "search_results": FeatureData[PairwiseAlignmentMN2],
    "reference_taxonomy": FeatureData[Taxonomy],
}
find_consensus_annotation_params = {
    "min_consensus": Float % Range(0.5, 1.0, inclusive_end=True, inclusive_start=False),
    "unassignable_label": Str,
}
find_consensus_annotation_params_dsc = {
    "min_consensus": "Minimum fraction of assignments must match top "
    "hit to be accepted as consensus assignment.",
    "unassignable_label": "Annotation given when no consensus is found.",
}
find_consensus_annotation_outputs = [("consensus_taxonomy", FeatureData[Taxonomy])]
find_consensus_annotation_inputs_dsc = {
    "search_results": "Search results in PairwiseAlignmentMN2 output format",
    "reference_taxonomy": "Reference taxonomy labels.",
}
find_consensus_annotation_outputs_dsc = {
    "consensus_taxonomy": "Consensus taxonomy and scores."
}
find_consensus_annotation_dsc = (
    "Find consensus annotation for each query searched against "
    "a reference database, by finding the least common ancestor "
    "among one or more semicolon-delimited hierarchical "
    "annotations. Note that the annotation hierarchy is assumed "
    "to have an even number of ranks."
)

# stats
T = TypeMatch([SequencesWithQuality, PairedEndSequencesWithQuality])
stats_inputs = {"sequences": SampleData[T]}
stats_input_descriptions = {"sequences": "Sequences to be analyzed."}
stats_dsc = "Quality control statistics of long sequences using NanoPlot."

# trim
trim_inputs = {"query_reads": SampleData[T]}
trim_outputs = [("filtered_query_reads", SampleData[T])]
trim_parameters = {
    "threads": Int % Range(1, None),
    "quality": Int % Range(0, None),
    "maxqual": Int % Range(0, None),
    "minlength": Int % Range(1, None),
    "maxlength": Int % Range(1, None),
    "headcrop": Int % Range(0, None),
    "tailcrop": Int % Range(0, None),
}
trim_input_descriptions = {"query_reads": "Sequences to be trimmed."}
trim_output_descriptions = {"filtered_query_reads": "The resulting trimmed sequences."}
trim_parameter_descriptions = {
    "threads": "Number of threads.",
    "quality": "Sets a minimum Phred average quality score.",
    "maxqual": "Sets a maximum Phred average quality score.",
    "minlength": "Sets a minimum read length.",
    "maxlength": "Sets a maximum read length.",
    "headcrop": "Trim N nucleotides from the start of a read.",
    "tailcrop": "Trim N nucleotides from the end of a read.",
}
trim_dsc = "Trim long demultiplexed sequences using Chopper tool."
