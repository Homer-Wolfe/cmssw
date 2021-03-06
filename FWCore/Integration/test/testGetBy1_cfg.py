import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD1")

process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )

process.source = cms.Source("IntSource")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(3)
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('testGetBy1.root'),
    outputCommands = cms.untracked.vstring(
        'keep *', 
        'drop *_intProducerA_*_*'
    )
)

process.a1 = cms.EDAnalyzer("TestFindProduct",
  inputTags = cms.untracked.VInputTag( cms.InputTag("source") ),
  expectedSum = cms.untracked.int32(12),
  inputTagsNotFound = cms.untracked.VInputTag(
    cms.InputTag("source", skipCurrentProcess = True),
    cms.InputTag("intProducer", skipCurrentProcess = True),
    cms.InputTag("intProducerU", skipCurrentProcess = True)
  )
)

process.a2 = cms.EDAnalyzer("TestFindProduct",
  inputTags = cms.untracked.VInputTag( cms.InputTag("intProducerA") ),
  expectedSum = cms.untracked.int32(300)
)

process.a3 = cms.EDAnalyzer("TestFindProduct",
  inputTags = cms.untracked.VInputTag( cms.InputTag("aliasForInt") ),
  expectedSum = cms.untracked.int32(300)
)

process.intProducer = cms.EDProducer("IntProducer", ivalue = cms.int32(1))

process.intProducerU = cms.EDProducer("IntProducer", ivalue = cms.int32(10))

process.intProducerA = cms.EDProducer("IntProducer", ivalue = cms.int32(100))

process.aliasForInt = cms.EDAlias(
  intProducerA  = cms.VPSet(
    cms.PSet(type = cms.string('edmtestIntProduct')
    )
  )
)

process.intVectorProducer = cms.EDProducer("IntVectorProducer",
  count = cms.int32(9),
  ivalue = cms.int32(11)
)

process.p = cms.Path(process.intProducer * process.a1 * process.a2 * process.a3)

process.e = cms.EndPath(process.out)
