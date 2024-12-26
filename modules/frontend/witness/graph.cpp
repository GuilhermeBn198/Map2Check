/**
 * Copyright (C) 2014 - 2019 Map2Check tool
 * This file is part of the Map2Check tool, and is made available under
 * the terms of the GNU General Public License version 2.
 *
 * BOOST     -> BSL-1.0
 *
 * SPDX-License-Identifier: (GPL-2.0 AND BSL-1.0)
 **/

#include <fstream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "graph.hpp"

#include <boost/make_unique.hpp>

#include "../utils/log.hpp"
#include "../utils/tools.hpp"
#include "witness.hpp"

// using namespace Map2Check;
using Map2Check::CorrectnessWitnessGraph;
using Map2Check::DataElement;
using Map2Check::Edge;
using Map2Check::Graph;
using Map2Check::Node;
using Map2Check::SVCompWitness;
using Map2Check::ViolationWitnessGraph;

namespace Tools = Map2Check;

using std::ofstream;

void Graph::AddElement(std::unique_ptr<DataElement> element) {
  this->elements.push_back(std::move(element));
}

void Graph::AddNode(std::unique_ptr<Node> node) {
  this->states.push_back(std::move(node));
}

void Graph::AddEdge(std::unique_ptr<Edge> edge) {
  this->transitions.push_back(std::move(edge));
}

std::string Graph::convertToString() {
  std::ostringstream cnvt;
  cnvt.str("");

  return cnvt.str();
}

std::string ViolationWitnessGraph::convertToString() {
  std::ostringstream cnvt;
  cnvt.str("");
  cnvt << "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n";
  cnvt << "<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\" "
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n";

  cnvt << "\t<key attr.name=\"isEntryNode\" attr.type=\"boolean\" for=\"node\" "
          "id=\"entry\">\n";
  cnvt << "\t\t<default>false</default>\n";
  cnvt << "\t</key>\n";
  cnvt << "\t<key attr.name=\"invariant\" attr.type=\"string\" for=\"node\" "
          "id=\"invariant\"/>\n";

  cnvt << "\t<key attr.name=\"isViolationNode\" attr.type=\"boolean\" "
          "for=\"node\" id=\"violation\">\n";
  cnvt << "\t\t<default>false</default>\n";
  cnvt << "\t</key>\n";

  cnvt << "\t<key attr.name=\"witness-type\" attr.type=\"string\" "
          "for=\"graph\" id=\"witness-type\"/>\n";
  cnvt << "\t<key attr.name=\"sourcecodelang\" attr.type=\"string\" "
          "for=\"graph\" id=\"sourcecodelang\"/>\n";
  cnvt << "\t<key attr.name=\"producer\" attr.type=\"string\" for=\"graph\" "
          "id=\"producer\"/>\n";
  cnvt << "\t<key attr.name=\"specification\" attr.type=\"string\" "
          "for=\"graph\" id=\"specification\"/>\n";
  cnvt << "\t<key attr.name=\"programFile\" attr.type=\"string\" for=\"graph\" "
          "id=\"programfile\"/>\n";
  cnvt << "\t<key attr.name=\"programHash\" attr.type=\"string\" for=\"graph\" "
          "id=\"programhash\"/>\n";
  cnvt << "\t<key attr.name=\"architecture\" attr.type=\"string\" "
          "for=\"graph\" id=\"architecture\"/>\n";

  cnvt << "\t<key attr.name=\"startline\" attr.type=\"int\" for=\"edge\" "
          "id=\"startline\"/>\n";
  cnvt << "\t<key attr.name=\"sourcecode\" attr.type=\"string\" for=\"edge\" "
          "id=\"sourcecode\"/>\n";
  cnvt << "\t<key attr.name=\"control\" attr.type=\"string\" for=\"edge\" "
          "id=\"control\"/>\n";
  cnvt << "\t<key attr.name=\"assumption\" attr.type=\"string\" for=\"edge\" "
          "id=\"assumption\"/>\n";
  cnvt << "\t<key attr.name=\"assumption.scope\" attr.type=\"string\" "
          "for=\"edge\" id=\"assumption.scope\"/>\n";
  cnvt << "\t<key attr.name=\"assumption.resultfunction\" attr.type=\"string\" "
          "for=\"edge\" id=\"assumption.resultfunction\"/>\n";

  cnvt << "\t<graph edgedefault=\"directed\">\n";

  for (int i = 0; i < this->elements.size(); i++) {
    cnvt << (std::string) * this->elements[i];
    cnvt << "\n";
  }

  for (int i = 0; i < this->states.size(); i++) {
    cnvt << (std::string) * this->states[i];
    cnvt << "\n";
  }

  for (int i = 0; i < this->transitions.size(); i++) {
    cnvt << (std::string) * this->transitions[i];
    cnvt << "\n";
  }

  cnvt << "\t</graph>\n";
  cnvt << "</graphml>";

  return cnvt.str();
}

std::string CorrectnessWitnessGraph::convertToString() {
  std::ostringstream cnvt;
  cnvt.str("");
  cnvt << "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n";
  cnvt << "<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\" "
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n";

  cnvt << "\t<key attr.name=\"isEntryNode\" attr.type=\"boolean\" for=\"node\" "
          "id=\"entry\">\n";
  cnvt << "\t\t<default>false</default>\n";
  cnvt << "\t</key>\n";
  cnvt << "\t<key attr.name=\"invariant\" attr.type=\"string\" for=\"node\" "
          "id=\"invariant\"/>\n";

  cnvt << "\t<key attr.name=\"witness-type\" attr.type=\"string\" "
          "for=\"graph\" id=\"witness-type\"/>\n";
  cnvt << "\t<key attr.name=\"sourcecodelang\" attr.type=\"string\" "
          "for=\"graph\" id=\"sourcecodelang\"/>\n";
  cnvt << "\t<key attr.name=\"producer\" attr.type=\"string\" for=\"graph\" "
          "id=\"producer\"/>\n";
  cnvt << "\t<key attr.name=\"specification\" attr.type=\"string\" "
          "for=\"graph\" id=\"specification\"/>\n";
  cnvt << "\t<key attr.name=\"programFile\" attr.type=\"string\" for=\"graph\" "
          "id=\"programfile\"/>\n";
  cnvt << "\t<key attr.name=\"programHash\" attr.type=\"string\" for=\"graph\" "
          "id=\"programhash\"/>\n";
  cnvt << "\t<key attr.name=\"architecture\" attr.type=\"string\" "
          "for=\"graph\" id=\"architecture\"/>\n";

  cnvt << "\t<key attr.name=\"startline\" attr.type=\"int\" for=\"edge\" "
          "id=\"startline\"/>\n";
  cnvt << "\t<key attr.name=\"sourcecode\" attr.type=\"string\" for=\"edge\" "
          "id=\"sourcecode\"/>\n";
  cnvt << "\t<key attr.name=\"control\" attr.type=\"string\" for=\"edge\" "
          "id=\"control\"/>\n";
  cnvt << "\t<key attr.name=\"assumption\" attr.type=\"string\" for=\"edge\" "
          "id=\"assumption\"/>\n";
  cnvt << "\t<key attr.name=\"assumption.scope\" attr.type=\"string\" "
          "for=\"edge\" id=\"assumption.scope\"/>\n";
  cnvt << "\t<key attr.name=\"assumption.resultfunction\" attr.type=\"string\" "
          "for=\"edge\" id=\"assumption.resultfunction\"/>\n";

  cnvt << "\t<graph edgedefault=\"directed\">\n";

  for (int i = 0; i < this->elements.size(); i++) {
    cnvt << (std::string) * this->elements[i];
    cnvt << "\n";
  }

  for (int i = 0; i < this->states.size(); i++) {
    cnvt << (std::string) * this->states[i];
    cnvt << "\n";
  }

  for (int i = 0; i < this->transitions.size(); i++) {
    cnvt << (std::string) * this->transitions[i];
    cnvt << "\n";
  }

  cnvt << "\t</graph>\n";
  cnvt << "</graphml>";

  return cnvt.str();
}

void SVCompWitness::Testify() {
  ofstream outputFile("../witness.graphml");
  // cout << (std::string) (*this->automata) << "\n" ;
  outputFile << (std::string)(*this->automata);
}

SVCompWitness::SVCompWitness(std::string programPath, std::string programHash,
                             std::string targetFunction,
                             std::string specTrueString) {
  Map2Check::Log::Debug("Starting Witness Generation");
  this->programHash = programHash;
  std::unique_ptr<DataElement> specification;
  Tools::CheckViolatedProperty violated;
  bool violationWitness = true;
  // TODO(hbgit): Add the inspection to automata true, what is the property was
  // I checking?
  switch (violated.propertyViolated) {
    case Tools::PropertyViolated::FALSE_FREE:
      specification =
          boost::make_unique<Specification>(SpecificationType::FREE);
      this->automata = boost::make_unique<ViolationWitnessGraph>();
      break;
    case Tools::PropertyViolated::FALSE_DEREF:
      specification =
          boost::make_unique<Specification>(SpecificationType::DEREF);
      this->automata = boost::make_unique<ViolationWitnessGraph>();
      break;
    case Tools::PropertyViolated::FALSE_MEMTRACK:
      specification =
          boost::make_unique<Specification>(SpecificationType::MEMLEAK);
      this->automata = boost::make_unique<ViolationWitnessGraph>();
      break;
    case Tools::PropertyViolated::TARGET_REACHED:
      specification = boost::make_unique<Specification>(
          SpecificationType::TARGET, targetFunction);
      this->automata = boost::make_unique<ViolationWitnessGraph>();
      break;
    case Tools::PropertyViolated::FALSE_OVERFLOW:
      specification =
          boost::make_unique<Specification>(SpecificationType::SPECOVERFLOW);
      this->automata = boost::make_unique<ViolationWitnessGraph>();
      break;
    default:
      this->automata = boost::make_unique<CorrectnessWitnessGraph>();
      violationWitness = false;
      break;
  }

  std::unique_ptr<DataElement> witnessType;

  if (violationWitness) {
    witnessType = boost::make_unique<WitnessType>(WitnessTypeValues::VIOLATION);
  } else {
    witnessType =
        boost::make_unique<WitnessType>(WitnessTypeValues::CORRECTNESS);
    if (specTrueString == "target-function") {
      // cout << specTrueString << "\n";
      specification = boost::make_unique<Specification>(
          SpecificationType::TARGET, targetFunction);
    } else if (specTrueString == "target-reach_error"){
      // cout << specTrueString << "\n";
      specification = boost::make_unique<Specification>(
          SpecificationType::TARGET_REACH_ERROR, targetFunction);
    } else if (specTrueString == "overflow") {
      specification =
          boost::make_unique<Specification>(SpecificationType::SPECOVERFLOW);
    } else {
      specification =
          boost::make_unique<Specification>(SpecificationType::MEMSAFETY);
    }
  }

  this->automata->AddElement(std::move(witnessType));

  std::unique_ptr<DataElement> sourceCodeType =
      boost::make_unique<SourceCodeLang>(SupportedSourceCodeLang::C);
  this->automata->AddElement(std::move(sourceCodeType));

  std::unique_ptr<DataElement> producer = boost::make_unique<Producer>();
  this->automata->AddElement(std::move(producer));

  this->automata->AddElement(std::move(specification));

  std::unique_ptr<DataElement> programFile =
      boost::make_unique<ProgramFile>(programPath);
  this->automata->AddElement(std::move(programFile));

  std::unique_ptr<DataElement> programHashElement =
      boost::make_unique<ProgramHash>(programHash);
  this->automata->AddElement(std::move(programHashElement));

  std::unique_ptr<DataElement> architecture =
      boost::make_unique<Architecture>(ArchitectureType::Bit32);
  this->automata->AddElement(std::move(architecture));

  if (violationWitness) {
    this->makeViolationAutomata();
  } else {
    this->makeCorrectnessAutomata();
  }
}

void SVCompWitness::makeCorrectnessSVComp() {
  Map2Check::Log::Info("Starting Correctness SVCOMP Generation");
  std::string lastStateId = "s0";
  std::unique_ptr<Node> startNode = boost::make_unique<Node>("s0");

  std::unique_ptr<NodeElement> entryNode = boost::make_unique<EntryNode>();
  startNode->AddElement(std::move(entryNode));
  this->automata->AddNode(std::move(startNode));
}

void SVCompWitness::makeCorrectnessAutomata() {
  Map2Check::Log::Debug("Starting Correctness Automata Generation");
  unsigned runState = 0;
  std::ostringstream cnvt;
  cnvt.str("");
  cnvt << "s" << runState;

  std::unique_ptr<Node> startNode = boost::make_unique<Node>(cnvt.str());
  std::string lastStateId;  // = "s0";
  runState++;               // s1

  std::unique_ptr<NodeElement> entryNode = boost::make_unique<EntryNode>();
  startNode->AddElement(std::move(entryNode));

  std::vector<Tools::StateTrueLogRow> stateTrueLogRows =
      Tools::StateTrueLogHelper::getListLogFromCSV();

// Removing the error location
//--- remove rows with error location
std:
  vector<int> removeItem;
  for (int c = 0; c < stateTrueLogRows.size(); c++) {
    if (stateTrueLogRows[c].isErrorLabel == "1") {
      removeItem.push_back(c);
    }
  }

  vector<int>::iterator iremove = removeItem.begin();
  while (iremove != removeItem.end()) {
    // cout << *iremove << "\n";
    stateTrueLogRows.erase(stateTrueLogRows.begin() + *iremove);
    ++iremove;
  }
  //---

  std::vector<Tools::TrackBBLogRow> trackBBLogRows =
      Tools::TrackBBLogHelper::getListLogFromCSV();

  if (stateTrueLogRows.size() == 0 || trackBBLogRows.size() == 0) {
    std::unique_ptr<Node> newNode = boost::make_unique<Node>("s1");
    std::unique_ptr<Edge> newEdge = boost::make_unique<Edge>("s0", "s1");
    this->automata->AddEdge(std::move(newEdge));
    this->automata->AddNode(std::move(newNode));
  }

  this->automata->AddNode(std::move(startNode));

  /**
   * Creating the automata nodes
   * The total number of automata nodes is equal to number lines in
   * automata_list_log.st file take into accounting the BB executed in
   * track_bb_log.st file
   * */

  unsigned runSearchIndx = 0;
  int lastK = 0;

  for (int i = 0; i < trackBBLogRows.size(); i++) {
    int trackBBLineNum = std::stoi(trackBBLogRows[i].numLineInBB);
    std::string trackBBFunctName = trackBBLogRows[i].functionName;
    bool flagCreateNewNode = false;

    int stateTrueNumLineBeginBB;
    int stateTrueNumLineStart;

    bool searchLineBB = true;

    // Checking if the state in stateTrueLogRows was executed in TrackBBLogRow
    // for(int k = lastK; (k < stateTrueLogRows.size() && searchLineBB); k++)
    for (int k = 0; (k < stateTrueLogRows.size() && searchLineBB); k++) {
      stateTrueNumLineBeginBB = std::stoi(stateTrueLogRows[k].numLineBeginBB);
      stateTrueNumLineStart = std::stoi(stateTrueLogRows[k].numLineStart);

      if (trackBBFunctName == stateTrueLogRows[k].functionName) {
        if ((trackBBLineNum >= stateTrueNumLineBeginBB) &&
            (trackBBLineNum <= stateTrueNumLineStart)) {
          searchLineBB = false;  // Stop search
          lastK = k + 1;

          lastStateId = cnvt.str();

          cnvt.str("");
          cnvt << "s" << runState;
          std::string tmpLastStateId;

          // This state (i.e., the BB) was executed
          // CREATING NODE
          tmpLastStateId = lastStateId;
          std::unique_ptr<Node> newNode = boost::make_unique<Node>(cnvt.str());
          runState++;

          // Create the edge to the new node
          std::unique_ptr<Edge> newEdge =
              boost::make_unique<Edge>(lastStateId, cnvt.str());

          // attribute startline
          std::unique_ptr<EdgeData> startLine = boost::make_unique<StartLine>(
              std::to_string(stateTrueNumLineStart));
          newEdge->AddElement(std::move(startLine));

          if (std::stoi(stateTrueLogRows[k].hasControlCode)) {
            //// search in trackBBLogRows which condition (TRUE or FALSE) by
            /// line number in / stateTrueLogRows was executed
            int tmpi = i + 1;  // next line of trackBBLogRows
            bool lastTrackBBLogRow = false;
            // last postion of trackBBLogRows
            if (tmpi >= trackBBLogRows.size()) {
              tmpi--;
              lastTrackBBLogRow = true;
            }

            bool hasTrueCond = false;

            //////=============== TRUE COND
            if (i < trackBBLogRows.size()) {
              if (std::stoi(stateTrueLogRows[k].numLineControlTrue) ==
                  std::stoi(trackBBLogRows[tmpi].numLineInBB)) {
                hasTrueCond = true;
                // create edge
                // attribute sourcecode
                std::unique_ptr<EdgeData> sourcecode =
                    boost::make_unique<SourceCode>(
                        stateTrueLogRows[k].controlCode);
                newEdge->AddElement(std::move(sourcecode));
                // attribute control
                std::unique_ptr<EdgeData> control =
                    boost::make_unique<Control>("condition-true");
                newEdge->AddElement(std::move(control));
                this->automata->AddEdge(std::move(newEdge));
              } else if (tmpi < trackBBLogRows.size() && !hasTrueCond) {
                ////=============== FALSE COND

                /**
                 *  creating a edge to its negation
                 *  create a new node, only if we have a false cond, otherwise
                 *we point to the same node from true cond
                 * */
                // attribute sourcecode
                std::string falseSourceCond =
                    "[!" + stateTrueLogRows[k].controlCode + "]";
                std::unique_ptr<EdgeData> sourcecodeF =
                    boost::make_unique<SourceCode>(falseSourceCond);
                newEdge->AddElement(std::move(sourcecodeF));
                // attribute control
                std::unique_ptr<EdgeData> controlF =
                    boost::make_unique<Control>("condition-false");
                newEdge->AddElement(std::move(controlF));
                this->automata->AddEdge(std::move(newEdge));
              }

              // last postion with control
              if (lastTrackBBLogRow) {
                i--;
              }
            }

          } else {
            // attribute sourcecode
            std::unique_ptr<EdgeData> sourcecode =
                boost::make_unique<SourceCode>(stateTrueLogRows[k].sourceCode);
            newEdge->AddElement(std::move(sourcecode));
            this->automata->AddEdge(std::move(newEdge));
          }

          this->automata->AddNode(std::move(newNode));
        }
      }
    }
  }
}

// when we don't have KLEE values
void SVCompWitness::makeViolationAutomataAux() {
  Map2Check::Log::Info("Starting Violation Automata Generation Mode 2");
  unsigned runState = 0;
  std::ostringstream cnvt;
  cnvt.str("");
  cnvt << "s" << runState;

  std::unique_ptr<Node> startNode = boost::make_unique<Node>(cnvt.str());
  std::string lastStateId;  // = "s0";
  runState++;               // s1

  std::unique_ptr<NodeElement> entryNode = boost::make_unique<EntryNode>();
  startNode->AddElement(std::move(entryNode));

  std::vector<Tools::StateTrueLogRow> stateTrueLogRows =
      Tools::StateTrueLogHelper::getListLogFromCSV();

  // The only difference that is not removed the error location

  std::vector<Tools::TrackBBLogRow> trackBBLogRows =
      Tools::TrackBBLogHelper::getListLogFromCSV();

  if (stateTrueLogRows.size() == 0 || trackBBLogRows.size() == 0) {
    std::unique_ptr<Node> newNode = boost::make_unique<Node>("s1");
    std::unique_ptr<Edge> newEdge = boost::make_unique<Edge>("s0", "s1");
    std::unique_ptr<NodeElement> violationNode =
        boost::make_unique<ViolationNode>();
    newNode->AddElement(std::move(violationNode));
    this->automata->AddEdge(std::move(newEdge));
    this->automata->AddNode(std::move(newNode));
  }

  this->automata->AddNode(std::move(startNode));

  /**
   * Creating the automata nodes
   * The total number of automata nodes is equal to number lines in
   * automata_list_log.st file take into accounting the BB executed in
   * track_bb_log.st file
   * */

  unsigned runSearchIndx = 0;
  int lastK = 0;

  for (int i = 0; i < trackBBLogRows.size(); i++) {
    int trackBBLineNum = std::stoi(trackBBLogRows[i].numLineInBB);
    std::string trackBBFunctName = trackBBLogRows[i].functionName;
    bool flagCreateNewNode = false;

    int stateTrueNumLineBeginBB;
    int stateTrueNumLineStart;

    bool searchLineBB = true;

    // Checking if the state in stateTrueLogRows was executed in TrackBBLogRow
    // for(int k = lastK; (k < stateTrueLogRows.size() && searchLineBB); k++)
    for (int k = 0; (k < stateTrueLogRows.size() && searchLineBB); k++) {
      stateTrueNumLineBeginBB = std::stoi(stateTrueLogRows[k].numLineBeginBB);
      stateTrueNumLineStart = std::stoi(stateTrueLogRows[k].numLineStart);

      if (trackBBFunctName == stateTrueLogRows[k].functionName) {
        if ((trackBBLineNum >= stateTrueNumLineBeginBB) &&
            (trackBBLineNum <= stateTrueNumLineStart)) {
          searchLineBB = false;  // Stop search
          lastK = k + 1;

          lastStateId = cnvt.str();

          cnvt.str("");
          cnvt << "s" << runState;
          std::string tmpLastStateId;

          // This state (i.e., the BB) was executed
          // CREATING NODE
          tmpLastStateId = lastStateId;
          std::unique_ptr<Node> newNode = boost::make_unique<Node>(cnvt.str());
          runState++;

          // Create the edge to the new node
          std::unique_ptr<Edge> newEdge =
              boost::make_unique<Edge>(lastStateId, cnvt.str());

          // attribute startline
          std::unique_ptr<EdgeData> startLine = boost::make_unique<StartLine>(
              std::to_string(stateTrueNumLineStart));
          newEdge->AddElement(std::move(startLine));

          if (std::stoi(stateTrueLogRows[k].hasControlCode)) {
            //// search in trackBBLogRows which condition (TRUE or FALSE) by
            /// line number in / stateTrueLogRows was executed
            int tmpi = i + 1;  // next line of trackBBLogRows
            bool lastTrackBBLogRow = false;
            // last postion of trackBBLogRows
            if (tmpi >= trackBBLogRows.size()) {
              tmpi--;
              lastTrackBBLogRow = true;
            }

            bool hasTrueCond = false;

            //////=============== TRUE COND
            if (i < trackBBLogRows.size()) {
              if (std::stoi(stateTrueLogRows[k].numLineControlTrue) ==
                  std::stoi(trackBBLogRows[tmpi].numLineInBB)) {
                hasTrueCond = true;
                // create edge
                // attribute sourcecode
                std::unique_ptr<EdgeData> sourcecode =
                    boost::make_unique<SourceCode>(
                        stateTrueLogRows[k].controlCode);
                newEdge->AddElement(std::move(sourcecode));
                // attribute control
                std::unique_ptr<EdgeData> control =
                    boost::make_unique<Control>("condition-true");
                newEdge->AddElement(std::move(control));
                this->automata->AddEdge(std::move(newEdge));
              } else if (tmpi < trackBBLogRows.size() && !hasTrueCond) {
                ////=============== FALSE COND

                /**
                 *  creating a edge to its negation
                 *  create a new node, only if we have a false cond, otherwise
                 *we point to the same node from true cond
                 * */
                // attribute sourcecode
                std::string falseSourceCond =
                    "[!" + stateTrueLogRows[k].controlCode + "]";
                std::unique_ptr<EdgeData> sourcecodeF =
                    boost::make_unique<SourceCode>(falseSourceCond);
                newEdge->AddElement(std::move(sourcecodeF));
                // attribute control
                std::unique_ptr<EdgeData> controlF =
                    boost::make_unique<Control>("condition-false");
                newEdge->AddElement(std::move(controlF));
                this->automata->AddEdge(std::move(newEdge));
              }

              // last postion with control
              if (lastTrackBBLogRow) {
                i--;
              }
            }

          } else {
            // attribute sourcecode
            std::unique_ptr<EdgeData> sourcecode =
                boost::make_unique<SourceCode>(stateTrueLogRows[k].sourceCode);
            newEdge->AddElement(std::move(sourcecode));
            this->automata->AddEdge(std::move(newEdge));
          }

          if (i == trackBBLogRows.size() - 1) {
            std::unique_ptr<NodeElement> violationNode =
                boost::make_unique<ViolationNode>();
            newNode->AddElement(std::move(violationNode));
          }
          this->automata->AddNode(std::move(newNode));
        }
      }
    }
  }
}

void SVCompWitness::makeViolationAutomata() {
  Map2Check::Log::Debug("Starting Violation Automata Generation");
  unsigned lastState = 0;
  std::string lastStateId = "s0";
  std::unique_ptr<Node> startNode = boost::make_unique<Node>("s0");
  lastState++;

  std::unique_ptr<NodeElement> entryNode = boost::make_unique<EntryNode>();
  startNode->AddElement(std::move(entryNode));

  std::vector<Tools::KleeLogRow> kleeLogRows =
      Tools::KleeLogHelper::getListLogFromCSV();
  std::vector<Tools::ListLogRow> listLogRows =
      Tools::ListLogHelper::getListLogFromCSV();
  // for target function error
  std::vector<Tools::TrackBBLogRow> trackBBLogRows =
      Tools::TrackBBLogHelper::getListLogFromCSV();

  if (kleeLogRows.size() == 0 && listLogRows.size() == 0 &&
      trackBBLogRows.size() == 0) {
    Tools::CheckViolatedProperty violated;
    // cout << violated.line << "\n";

    this->automata->AddNode(std::move(startNode));  // s0

    std::unique_ptr<Node> newNode = boost::make_unique<Node>("s1");
    std::unique_ptr<NodeElement> violationNode =
        boost::make_unique<ViolationNode>();
    newNode->AddElement(std::move(violationNode));

    std::unique_ptr<Edge> newEdge = boost::make_unique<Edge>("s0", "s1");
    // attribute startline
    std::unique_ptr<EdgeData> startLine =
        boost::make_unique<StartLine>(std::to_string(violated.line));
    newEdge->AddElement(std::move(startLine));

    this->automata->AddEdge(std::move(newEdge));
    this->automata->AddNode(std::move(newNode));

  } else if (kleeLogRows.size() == 0 &&
             (listLogRows.size() > 0 || trackBBLogRows.size() > 0)) {
    // this->automata->AddNode(std::move(startNode));
    this->makeViolationAutomataAux();
  } else {
    this->automata->AddNode(std::move(startNode));

    for (int i = 0; i < kleeLogRows.size(); i++) {
      std::string lineNumber = kleeLogRows[i].line;
      std::string value = kleeLogRows[i].value;
      std::string functionName = kleeLogRows[i].functionName;

      std::ostringstream cnvt;
      cnvt.str("");
      cnvt << "s" << lastState;
      lastState++;

      std::unique_ptr<Node> newNode = boost::make_unique<Node>(cnvt.str());
      if (i == (kleeLogRows.size() - 1)) {
        std::unique_ptr<NodeElement> violationNode =
            boost::make_unique<ViolationNode>();
        newNode->AddElement(std::move(violationNode));
      }

      this->automata->AddNode(std::move(newNode));

      std::unique_ptr<Edge> newEdge =
          boost::make_unique<Edge>(lastStateId, cnvt.str());
      lastStateId = cnvt.str();

      std::unique_ptr<EdgeData> assumption =
          boost::make_unique<AssumptionEdgeData>(
              value, kleeLogRows[i].generateWitnessFunctionName(),
              functionName);
      newEdge->AddElement(std::move(assumption));

      std::unique_ptr<EdgeData> startLine =
          boost::make_unique<StartLine>(lineNumber);
      newEdge->AddElement(std::move(startLine));

      this->automata->AddEdge(std::move(newEdge));
    }
  }
}
