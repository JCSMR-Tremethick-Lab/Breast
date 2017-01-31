_author__ = "Sebastian Kurscheid (sebastian.kurscheid@anu.edu.au)"
__license__ = "MIT"
__date__ = "2016-12-05"

from snakemake.exceptions import MissingInputException
import os

rule:
    version: 0.1

localrules:
    all, run_kallisto, run_STAR, run_htseq, run_cutadapt

home = os.environ['HOME']

wrapper_dir = home + "/Development/snakemake-wrappers/bio"

include_prefix = home + "/Development/JCSMR-Tremethick-Lab/Breast/snakemake/rules/"

# include:
#    include_prefix + "perform_cutadapt.py"
# include:
#     include_prefix + "run_bowtie2.py"
include:
    include_prefix + "bam_processing.py"
include:
    include_prefix + "run_deepTools_QC.py"
include:
    include_prefix + "run_deepTools.py"

# define global variables such as reference version of genome so that it can be accessed
# throughout the whole worfklow
REF_GENOME = config["references"]["genomes"][1]

rule run_cutadapt:
    input:
        expand("{assayID}/{runID}/{outdir}/{trim_data}/{unit}_{suffix}.QT.CA.fastq.gz",
               assayID = "ChIP-Seq",
               runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
               outdir = config["processed_dir"],
               trim_data = config["trim_dir"],
               unit = config["samples"]["ChIP-Seq"]["SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq"],
               suffix = ["R1_001", "R2_001"]),
        expand("{assayID}/{runID}/{outdir}/{trim_data}/{unit}_{suffix}.QT.CA.fastq.gz",
               assayID = "ChIP-Seq",
               runID = "NB501086_0086_DSTremethick_JCSMR_MCF10A_ChIPseq",
               outdir = config["processed_dir"],
               trim_data = config["trim_dir"],
               unit = config["samples"]["ChIP-Seq"]["NB501086_0086_DSTremethick_JCSMR_MCF10A_ChIPseq"],
               suffix = ["R1_001", "R2_001"])

rule deepTools_QC:
    input:
        expand("{assayID}/{outdir}/{reference_version}/deepTools/plotCorrelation/{duplicates}/heatmap_SpearmanCorr_readCounts.{suffix}",
               assayID = "ChIP-Seq",
               runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
               outdir = config["processed_dir"],
               reference_version = config["references"][REF_GENOME]["version"][0],
               duplicates = ["duplicates_marked", "duplicates_removed"],
               suffix = ["png", "tab"]),
        expand("{assayID}/{outdir}/{reference_version}/deepTools/plotPCA/{duplicates}/PCA_readCounts.png",
               assayID = "ChIP-Seq",
               runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
               outdir = config["processed_dir"],
               reference_version = config["references"][REF_GENOME]["version"][0],
               duplicates = ["duplicates_marked", "duplicates_removed"]),
        expand("{assayID}/{outdir}/{reference_version}/deepTools/plotFingerprint/{duplicates}/fingerprints_{duplicates}.png",
               assayID = "ChIP-Seq",
               runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
               outdir = config["processed_dir"],
               reference_version = config["references"][REF_GENOME]["version"][0],
               duplicates = ["duplicates_marked"]),
        expand("{assayID}/{outdir}/{reference_version}/deepTools/bamPEFragmentSize/{duplicates}/histogram_{duplicates}.png",
               assayID = "ChIP-Seq",
               runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
               outdir = config["processed_dir"],
               reference_version = config["references"][REF_GENOME]["version"][0],
               duplicates = ["duplicates_marked"])

rule deepTools_QC_deduplicated:
    input:
        expand("{assayID}/{outdir}/{reference_version}/deepTools/plotFingerprint/{duplicates}/fingerprints_{duplicates}.png",
               assayID = "ChIP-Seq",
               runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
               outdir = config["processed_dir"],
               reference_version = config["references"][REF_GENOME]["version"][0],
               duplicates = ["duplicates_removed"]),
        expand("{assayID}/{outdir}/{reference_version}/deepTools/bamPEFragmentSize/{duplicates}/histogram_{duplicates}.png",
               assayID = "ChIP-Seq",
               runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
               outdir = config["processed_dir"],
               reference_version = config["references"][REF_GENOME]["version"][0],
               duplicates = ["duplicates_removed"])


rule all:
    input:
        # expand("{assayID}/{runID}/{outdir}/{reference_version}/bowtie2/duplicates_marked/{unit}.Q{qual}.sorted.MkDup.{suffix}",
        #        assayID = "ChIP-Seq",
        #        runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
        #        outdir = config["processed_dir"],
        #        reference_version = config["references"][REF_GENOME]["version"][0],
        #        unit = config["samples"]["ChIP-Seq"]["SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq"],
        #        qual = config["alignment_quality"],
        #        suffix = ["bam", "bam.bai"]),
        # expand("{assayID}/{runID}/{outdir}/{reference_version}/bowtie2/duplicates_marked/{unit}.Q{qual}.sorted.MkDup.{suffix}",
        #        assayID = "ChIP-Seq",
        #        runID = "NB501086_0086_DSTremethick_JCSMR_MCF10A_ChIPseq",
        #        outdir = config["processed_dir"],
        #        reference_version = config["references"][REF_GENOME]["version"][0],
        #        unit = config["samples"]["ChIP-Seq"]["NB501086_0086_DSTremethick_JCSMR_MCF10A_ChIPseq"],
        #        qual = config["alignment_quality"],
        #        suffix = ["bam", "bam.bai"]),
        # expand("{assayID}/{runID}/{outdir}/{reference_version}/bowtie2/duplicates_removed/{unit}.Q{qual}.sorted.DeDup.{suffix}",
        #        assayID = "ChIP-Seq",
        #        runID = "SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq",
        #        outdir = config["processed_dir"],
        #        reference_version = config["references"][REF_GENOME]["version"][0],
        #        unit = config["samples"]["ChIP-Seq"]["SN501_0087_DTremethick_JCSMR_MCF10A_ChIPSeq"],
        #        qual = config["alignment_quality"],
        #        suffix = ["bam", "bam.bai"]),
        # expand("{assayID}/{runID}/{outdir}/{reference_version}/bowtie2/duplicates_removed/{unit}.Q{qual}.sorted.DeDup.{suffix}",
        #        assayID = "ChIP-Seq",
        #        runID = "NB501086_0086_DSTremethick_JCSMR_MCF10A_ChIPseq",
        #        outdir = config["processed_dir"],
        #        reference_version = config["references"][REF_GENOME]["version"][0],
        #        unit = config["samples"]["ChIP-Seq"]["NB501086_0086_DSTremethick_JCSMR_MCF10A_ChIPseq"],
        #        qual = config["alignment_quality"],
        #        suffix = ["bam", "bam.bai"]),
        expand("{assayID}/{runID}/{outdir}/{reference_version}/{application}/{tool}/{command}/{duplicates}/{referencePoint}/{plotType}.{mode}.{region}.{suffix}",
               assayID = "ChIP-Seq",
               runID = "merged",
               outdir = config["processed_dir"],
               reference_version = config["references"][REF_GENOME]["version"][0],
               application = "deepTools",
               tool = "plotProfile",
               command = ["reference-point", "scale-regions"],
               duplicates = ["duplicates_marked", "duplicates_removed"],
               referencePoint = "TSS",
               plotType = "se",
               mode = ["MNase", "normal"],
               region = "allGenes",
               suffix = ["pdf", "data", "bed"])
