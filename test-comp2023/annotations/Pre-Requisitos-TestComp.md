# Competition Contributions Guidelines

- The competition contributions consist of three main parts:

  - **System Description**

  - **Executable Tool (Competition Candidate)**

  - **Benchmark Definition**

  - **Tool-info Module for BenchExec**

## System Description

The system description paper should ideally be structured as follows:

Title, Authors, and Abstract
The paper should follow the usual LNCS style. It's a good idea to mention the name of the tool and/or technique in the title. Mark the jury member in the paper with an asterisk after their name and a footnote robotframework.org.

- **Test-Generation Approach**
   1. **Software Architecture**
   Detail the libraries and external tools that the testing tool uses (e.g., parser frontend, SAT solver). Describe the software structure and architecture (e.g., components that are used in the competition) and the implementation technology (e.g., programming language).
   2. **Discussion of Strengths and Weaknesses of the Approach**
   3. **Tool Setup and Configuration**
    Provide download instructions (a public web page from which the tool can be downloaded) including a reference to a precise version of the tool (do not refer to "the latest version" or such, because that is not stable and not replicable). Include installation instructions and a participation statement (a clear statement which categories the tester participates in; consult the rules about opt-out statements). Configuration definition (there is one global set of parameters for all categories of the benchmark set, a full definition of the parameter set must be provided); check the rules page under Parameters for more details.
   4. **Software Project and Contributors**
    Provide contact info (web page of the project, people involved in the project), and information about the software project, licensing, development model, institution that hosts the software project, and acknowledgement of contributors.
   5. **Data-Availability Statement**
    Publish (e.g., on Zenodo) your tool archive and reference it here (via DOI) to ensure reproducibility, also provide the URL of the project web site and repository.
   6. **References**

## **Executable Tool (Competition Candidate)**

- with output files being the **test-suite.zip** containing the following files:
  - testcase.xml
  - metadata.xml

## **Benchmark Definition**
  
- In order to participate at Test-Comp, a benchmark definition in the Test-Comp repository is necessary. Technically, the benchmark definition needs to be integrated into the Test-Comp repository under directory benchmark-defs using a **merge request**.
- The name of the benchmark should also be mentioned in the **system description**.

## **Tool-info Module for BenchExec**

- In order to participate at Test-Comp, a tool-info module in the BenchExec repository is necessary. Technically, the tool-info module needs to be integrated into the BenchExec repository under directory benchexec/tools using a **pull request**.
- The name of this module **should be mentioned in the system description**.
