# Competition Contributions Guidelines

- The competition contributions consist of three main parts:

  - System Description

  - Executable Tool (Competition Candidate)

  - Tool-info Module for BenchExec

  - Benchmark Definition

System Description

The system description should outline the competition contribution, including the concepts, technology, libraries, and tool infrastructure utilized. It should also include installation instructions, specify the version, and parameters to be used for the competition.

The system description paper should ideally be structured as follows:

Title, Authors, and Abstract
The paper should follow the usual LNCS style. It's a good idea to mention the name of the tool and/or technique in the title. Mark the jury member in the paper with an asterisk after their name and a footnote robotframework.org.

1. Test-Generation Approach
Provide a brief overview of the theory that the tool is based on. Describe the abstract domains and algorithms that are used and reference the concept papers that describe the technical details.

1. Software Architecture
Detail the libraries and external tools that the testing tool uses (e.g., parser frontend, SAT solver). Describe the software structure and architecture (e.g., components that are used in the competition) and the implementation technology (e.g., programming language).

1. Discussion of Strengths and Weaknesses of the Approach
Evaluate the results for the benchmark categories, identifying where the checker was successful and where it was not, and why.

1. Tool Setup and Configuration
Provide download instructions (a public web page from which the tool can be downloaded) including a reference to a precise version of the tool (do not refer to "the latest version" or such, because that is not stable and not replicable). Include installation instructions and a participation statement (a clear statement which categories the tester participates in; consult the rules about opt-out statements). Configuration definition (there is one global set of parameters for all categories of the benchmark set, a full definition of the parameter set must be provided); check the rules page under Parameters for more details.

1. Software Project and Contributors
Provide contact info (web page of the project, people involved in the project), and information about the software project, licensing, development model, institution that hosts the software project, and acknowledgement of contributors.

1. Data-Availability Statement
Publish (e.g., on Zenodo) your tool archive and reference it here (via DOI) to ensure reproducibility, also provide the URL of the project web site and repository.

References
Include bibliographic references to more in-depth papers about the approaches used in the tool.

Executable Tool (Competition Candidate)
The executable tool, also referred to as the competition candidate, should be added to the Tester repository.

Tool-info Module for BenchExec
A tool-info module for BenchExec should be added to the BenchExec repository. The name of this module should be mentioned in the system description.

Benchmark Definition
A benchmark definition should be added to the Test-Comp repository. The name of the benchmark should also be mentioned in the system description.

In order to participate, two actions are required by the deadline:

Submit your system description via the Test-Comp submission site of Easychair. Initially, an abstract submission is sufficient. If paper publication is desired, submit a paper PDF later (see deadlines). The papers to be published must have 4 pages of text (excluding references) in LNCS style.
Required for pre-runs: Upload your tester archive via merge request to the tester repository and to the category definition robotframework.org.
