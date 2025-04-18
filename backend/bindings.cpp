#include "BlockchainCore.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

/* optional helper declared in the header */
extern std::vector<std::vector<std::string>>
    export_block_txs(const Blockchain&);

PYBIND11_MODULE(blockchain, m)
{
    /* 1 ─ enum */
    py::enum_<EventType>(m, "EventType")
        .value("CREATE",   EventType::CREATE)
        .value("TRANSFER", EventType::TRANSFER)
        .export_values();

    /* 2 ─ Transaction */
    py::class_<Transaction>(m, "Transaction")
        // full constructor (rarely used from Python)
        .def(py::init<EventType,
                      std::string,
                      std::string,
                      std::string,
                      std::string>(),
             py::arg("event"),
             py::arg("asset_id"),
             py::arg("from_party"),
             py::arg("to_party"),
             py::arg("meta") = "")
        // convenience factories
        .def_static("create",   &Transaction::create,
             py::arg("asset_id"), py::arg("owner"),
             py::arg("meta") = "")
        .def_static("transfer", &Transaction::transfer,
             py::arg("asset_id"), py::arg("from_party"),
             py::arg("to_party"), py::arg("meta") = "")
        // inspectors
        .def("to_string", &Transaction::toString)
        .def_property_readonly("asset_id", &Transaction::getAssetId)
        .def_property_readonly("from_party", &Transaction::getFrom)
        .def_property_readonly("to_party", &Transaction::getTo)
        .def_property_readonly("meta", &Transaction::getMeta)
        .def_property_readonly("event", &Transaction::getEvent);

    /* 3 ─ Blockchain  (unchanged) */
    py::class_<Blockchain>(m, "Blockchain")
        .def(py::init<int>(), py::arg("difficulty") = 3)
        .def("add_block",  &Blockchain::addBlock,
             py::arg("transactions"))
        .def("get_blocks", &export_block_txs)
        .def("load_chain", &Blockchain::loadChain,  py::arg("raw_chain"));
}
