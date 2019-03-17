frma = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/"
lio = "https://w3id.org/lio/v1#"


# treeClassQuery = """
#  select *
#  where{
#      ?class a owl:Class.
#      ?class rdfs:label ?name.
#
#       OPTIONAL {
#        ?class rdfs:subClassOf ?super .
#        ?super a owl:Class.
#           ?super rdfs:label ?super_name.
#       }
#      }
# """


correctQuery = "filter(?classification = ?Name)"
incorrectQuery = "filter(?classification != ?Name)"

treeClassQuery = """
prefix mlmo: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
prefix lio: <http://purl.org/net/lio#>
prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
prefix img: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/>
prefix frma: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/>
prefix pfd: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/>
prefix ho: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/>
prefix wt: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/WearableThingsOntology/>

select distinct ?class ?name ?super ?super_name
 where{
  {
    ?super rdfs:subClassOf ?restriction .
    ?restriction rdf:type owl:Restriction .
    ?restriction owl:someValuesFrom ?class .
	?class a owl:Class.
    ?class rdfs:label ?name.


    bind(<https://w3id.org/lio/v1#Image> AS ?super)
    bind("image" AS ?super_name)
    }
   union
   {
     ?class a owl:Class.
     ?class rdfs:label ?name.
   	 ?class rdfs:subClassOf ?super .

     bind(<https://w3id.org/lio/v1#Image> AS ?super)
     bind("image" AS ?super_name)
     }
   union
   {
     values (?class ?name ?super ?super_name){
     	(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/MugShotPhoto> "mug shot photo" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/PosedImage> "posed image")
        (<https://w3id.org/lio/v1#PictorialElement> "pictorial element" <https://w3id.org/lio/v1#Image> "image")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Demographic> "demographic" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/WearableThingsOntology/WearableObject> "wearable object" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/VisualDescriptor> "visual descriptor" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<http://purl.obolibrary.org/obo/UBERON_0001567> "cheek" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")

        (<http://purl.obolibrary.org/obo/UBERON_0008199> "chin" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/Hair> "hair" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person" <https://w3id.org/lio/v1#PictorialElement> "pictorial element")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HairColor> "hair color" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/Hair> "hair")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HairTexture> "hair texture" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HeadHair> "head hair")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/Haircut> "haircut" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HeadHair> "head hair")

        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/FacialExpression> "facial expression" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/FaceShape> "face shape" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/SkinTone> "skin tone" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
     }

     }
   union
   {

     ?class a owl:Class.
      ?class rdfs:label ?name.

       OPTIONAL {
        ?class rdfs:subClassOf ?super .
        ?super a owl:Class.
           ?super rdfs:label ?super_name.
       }
      }

   filter(img:ImageFile != ?class)
   filter(mlmo:Datum != ?super)
   filter(mlmo:Activity != ?super)
   filter(mlmo:Layer != ?super)
   filter(mlmo:Dataset != ?super)
   filter(mlmo:Model != ?super)
   filter(mlmo:NeuralNetwork != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0000475> != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0011676> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/ForheadVisibility> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/MouthOpenState> != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0001444> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/ForheadVisibility> != ?class)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/MouthOpenState> != ?class)

   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Finish> != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0000020> != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0000062> != ?super)

   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Color> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Color> != ?class)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Size> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/VisualDescriptor> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/VisualDescriptor> != ?class)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/NoseShape> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HairColor> != ?class)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/OptimalConditionImage> != ?class)

} ORDER BY ?super_name ?name
"""

baseQuery = """
    prefix mlmo: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
    prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
    prefix lio: <http://purl.org/net/lio#>
    prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
    prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
    prefix img: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/>
    prefix frma: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/>
    prefix pfd: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/>
    prefix ho: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/>
    prefix wt: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/WearableThingsOntology/>

    select distinct ?Image ?classification ?Name
        where {
          ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
          ?Result lcc-lr:hasTag ?classification .
          ?Result mlmo:hasFeature ?Image .
          ?Image lio:depicts ?Person .
          ?Person fibo-fnd-aap-a:hasName ?Name .
"""

prefix = """
    prefix mlmo: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
    prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
    prefix lio: <http://purl.org/net/lio#>
    prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
    prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
    prefix img: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/>
    prefix frma: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/>
    prefix pfd: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/>
    prefix ho: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/>
    prefix wt: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/WearableThingsOntology/>
"""

baseCountQuery = """
    select (count(distinct ?Image) as ?count)
        where {
          ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
          ?Result lcc-lr:hasTag ?classification .
          ?Result mlmo:hasFeature ?Image .
          ?Image lio:depicts ?Person .
          ?Person fibo-fnd-aap-a:hasName ?Name .
"""

baseAccQuery = """
    select ?numCorrect ?count
    where {
"""

baseNumCorrectQuery = """
    select (count(distinct ?classification) as ?numCorrect)
    where {
        ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
        ?Result mlmo:hasFeature ?Image .
        ?Image lio:depicts ?Person .
        ?Person fibo-fnd-aap-a:hasName ?Name .
        ?Result lcc-lr:hasTag ?classification .
        filter (?classification = ?Name)
"""

mugshotQuery = """
    ?Image a img:PosedImage.

    # Indoors
    ?Image lio:hasDepictedBackground ?background .
    ?background a img:Indoors .

    # No Face occlusions
    OPTIONAL{
      ?Image frma:hasOcclusion ?occlusion.
     }

     minus{
         ?occlusion a ?FaceOcclusionClass .
         ?FaceOcclusionClass rdfs:subClassOf* frma:FaceOcclusion .
     }

    # Image Fidelity not blurry
    ?Image img:fidelityDescribedBy ?fidelity .
    minus{
      ?fidelity a img:BlurryImageFidelity .
     }
"""
occlusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?occlusionClass .
    ?occlusionClass rdfs:subClassOf* frma:Occlusion .
"""

cervicalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?CervicalOcclusionClass .
    ?CervicalOcclusionClass rdfs:subClassOf* frma:CervicalOcclusion .
"""

FaceOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?FaceOcclusionClass .
    ?FaceOcclusionClass rdfs:subClassOf* frma:FaceOcclusion .
"""

LowerFaceOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?LowerFaceOcclusionClass .
    ?LowerFaceOcclusionClass rdfs:subClassOf* frma:LowerFaceOcclusion .
"""

UpperFaceOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?UpperFaceOcclusionClass .
    ?UpperFaceOcclusionClass rdfs:subClassOf* frma:UpperFaceOcclusion .
"""

BuccalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?BuccalOcclusionClass .
    ?BuccalOcclusionClass rdfs:subClassOf* frma:BuccalOcclusion .
"""

OralOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?OralOcclusionClass .
    ?OralOcclusionClass rdfs:subClassOf* frma:OralOcclusion .
"""

MentalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?MentalOcclusionClass .
    ?MentalOcclusionClass rdfs:subClassOf* frma:MentalOcclusion .
"""

ParotidOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?ParotidOcclusionClass .
    ?ParotidOcclusionClass rdfs:subClassOf* frma:ParotidOcclusion .
"""

ZygomaticOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?ZygomaticOcclusionClass .
    ?ZygomaticOcclusionClass rdfs:subClassOf* frma:ZygomaticOcclusion .
"""

AuricleOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?AuricleOcclusionClass .
    ?AuricleOcclusionClass rdfs:subClassOf* frma:AuricleOcclusion .
"""

CranialOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?CranialOcclusionClass .
    ?CranialOcclusionClass rdfs:subClassOf* frma:CranialOcclusion .
"""

FrontalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?FrontalOcclusionClass .
    ?FrontalOcclusionClass rdfs:subClassOf* frma:FrontalOcclusion .
"""

OcularOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?OcularOcclusionClass .
    ?OcularOcclusionClass rdfs:subClassOf* frma:OcularOcclusion .
"""

NasalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?NasalOcclusionClass .
    ?NasalOcclusionClass rdfs:subClassOf* frma:NasalOcclusion .
"""

CheekQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?cheek .
    ?Face a <http://purl.obolibrary.org/obo/UBERON_0001456> .
    ?cheek a ?cheekClass .
    ?cheekClass rdfs:subClassOf* <http://purl.obolibrary.org/obo/UBERON_0001567> .
"""

HighCheekQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?cheek .
    ?Face a <http://purl.obolibrary.org/obo/UBERON_0001456> .
    ?cheek a pfd:HighCheekbones .
"""

RosyCheekQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?cheek .
    ?Face a <http://purl.obolibrary.org/obo/UBERON_0001456> .
    ?cheek a pfd:RosyCheeks .
"""

ChinQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?chin .
    ?Face a <http://purl.obolibrary.org/obo/UBERON_0001456> .
    ?chin a <http://purl.obolibrary.org/obo/UBERON_0008199> .
"""

DoubleChinQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?chin .
    ?Face a <http://purl.obolibrary.org/obo/UBERON_0001456> .
    ?chin a pfd:DoubleChin .
"""

RoundJawQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?chin .
    ?Face a <http://purl.obolibrary.org/obo/UBERON_0001456> .
    ?chin a pfd:RoundJaw .
"""

DemographicQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a ?demoClass .
    ?demoClass rdfs:subClassOf* pfd:Demographic .
"""
AgeRangeQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a ?demoClass .
    ?demoClass rdfs:subClassOf* pfd:AgeRange .
"""
BabyQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Baby .
"""
ChildQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Child .
"""
MiddleAgedQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:MiddleAged .
"""
SeniorQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Senior .
"""
YouthQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Baby .
"""

EthnicityQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a ?demoClass .
    ?demoClass rdfs:subClassOf* pfd:Ethnicity .
"""
AsianQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Asian .
"""
BlackQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Black .
"""
IndianQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Indian .
"""
WhiteQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:White .
"""


GenderExpressionQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a ?demoClass .
    ?demoClass rdfs:subClassOf* pfd:GenderExpression .
"""
FeminineQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Feminine .
"""
MasculineQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Masculine .
"""


WeightRangeQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a ?demoClass .
    ?demoClass rdfs:subClassOf* pfd:WeightRange .
"""
SkinnyQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Skinny .
"""
ChubbyQuery = """
    ?Person pfd:hasDemographic ?Demo .
    ?Demo a pfd:Chubby .
"""

FaceShapeQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasShape ?FaceShape .
    ?FaceShape a pfd:FaceShape .
"""
OvalFaceQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasShape ?FaceShape .
    ?FaceShape a pfd:OvalFace .
"""
RoundFaceQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasShape ?FaceShape .
    ?FaceShape a pfd:RoundFace .
"""
SquareFaceQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasShape ?FaceShape .
    ?FaceShape a pfd:SquareFace .
"""

FacialExpressionQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasVisualFeature ?FacialExpression .
    ?FacialExpression a pfd:FacialExpression .
"""
ArchedEyebrowQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasVisualFeature ?FacialExpression .
    ?FacialExpression a pfd:ArchedEyebrow .
"""
FrowningQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasVisualFeature ?FacialExpression .
    ?FacialExpression a pfd:Frowning .
"""
NarrowEyesQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasVisualFeature ?FacialExpression .
    ?FacialExpression a pfd:NarrowEyes .
"""
SmilingQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face pfd:hasVisualFeature ?FacialExpression .
    ?FacialExpression a pfd:Smiling .
"""

HairQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair a ?hairClass .
    ?hairClass rdfs:subClassOf* ho:Hair .
"""
HeadHairQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair a ho:HeadHair .
"""
FacialHairQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair a ?hairClass .
    ?hairClass rdfs:subClassOf* ho:FacialHair .
"""

BeardQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Beard .
    ?Beard a ?beardClass .
    ?beardClass rdfs:subClassOf* ho:Beard .
"""
FiveOClockShadowQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Beard .
    ?Beard a ho:FiveOClockShadow .
"""
GoateeQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Beard .
    ?Beard a ho:Goatee .
"""

EyebrowsQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Eyebrows .
    ?Eyebrows a ?EyebrowsClass .
    ?EyebrowsClass rdfs:subClassOf* ho:Eyebrows .
"""
BushyEyebrowsQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Eyebrows .
    ?Eyebrows a ho:BushyEyebrows .
"""
ThinEyebrowsQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Eyebrows .
    ?Eyebrows a ho:ThinEyebrows .
"""

MustacheQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Mustache .
    ?Mustache a ho:Mustache .
"""
SideburnQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Sideburn .
    ?Sideburn a ho:Sideburn .
"""


HairTextureQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasTexture ?HairTexture .
    ?HairTexture a ?HairTextureClass .
    ?HairTextureClass rdfs:subClassOf* ho:HairTexture .
"""
CurlyHairQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasTexture ?HairTexture .
    ?HairTexture a ho:CurlyHair .
"""
StraightHairQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasTexture ?HairTexture .
    ?HairTexture a ho:StraightHair .
"""
WavyHairQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasTexture ?HairTexture .
    ?HairTexture a ho:WavyHair .
"""


HaircutQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasHaircut ?Haircut .
    ?Haircut a ?HaircutClass .
    ?HaircutClass rdfs:subClassOf* ho:Haircut .
"""
BaldingQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasHaircut ?Haircut .
    ?Haircut a ?HaircutClass .
    ?HaircutClass rdfs:subClassOf* ho:Balding .
"""
LongHairQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasHaircut ?Haircut .
    ?Haircut a ?HaircutClass .
    ?HaircutClass rdfs:subClassOf* ho:LongHair .
"""
BaldQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasHaircut ?Haircut .
    ?Haircut a ho:Bald .
"""
RecedingHairlineQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasHaircut ?Haircut .
    ?Haircut a ho:RecedingHairline .
"""
BangsQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Hair .
    ?Hair ho:hasHaircut ?Haircut .
    ?Haircut a ho:Bangs .
"""


SkinToneQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?Skin .
    ?Skin pfd:hasVisualFeature ?SkinTone.
    ?SkinTone a pfd:SkinTone .
"""
FlushQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?Skin .
    ?Skin pfd:hasVisualFeature ?SkinTone.
    ?SkinTone a pfd:Flush .
"""
PaleQuery = """
    ?Person <http://purl.obolibrary.org/obo/BFO_0000051> ?Face .
    ?Face <http://purl.obolibrary.org/obo/BFO_0000051> ?Skin .
    ?Skin pfd:hasVisualFeature ?SkinTone.
    ?SkinTone a pfd:Pale .
"""


WearableObjectQuery = """
    ?Person wt:isWearing ?WearableObject .
    ?WearableObject a ?WearableObjectClass .
    ?WearableObjectClass rdfs:subClassOf* wt:WearableObject .
"""
HeadwearQuery = """
    ?Person wt:isWearing ?Headwear .
    ?Headwear a ?HeadwearClass .
    ?HeadwearClass rdfs:subClassOf* wt:Headwear .
"""
EyewearQuery = """
    ?Person wt:isWearing ?Eyewear .
    ?Eyewear a ?EyewearClass .
    ?EyewearClass rdfs:subClassOf* wt:Eyewear .
"""
EyeglassesQuery = """
    ?Person wt:isWearing ?Eyeglasses .
    ?Eyeglasses a ?EyeglassesClass .
    ?EyeglassesClass rdfs:subClassOf* wt:Eyeglasses .
"""
SunglassesQuery = """
    ?Person wt:isWearing ?Sunglasses .
    ?Sunglasses a ?SunglassesClass .
    ?SunglassesClass rdfs:subClassOf* wt:Sunglasses .
"""
HatQuery = """
    ?Person wt:isWearing ?Hat .
    ?Hat a ?HatClass .
    ?HatClass rdfs:subClassOf* wt:Hat .
"""
OrnamentQuery = """
    ?Person wt:isWearing ?Ornament .
    ?Ornament a ?OrnamentClass .
    ?OrnamentClass rdfs:subClassOf* wt:Ornament .
"""
HeadwearQuery = """
    ?Person wt:isWearing ?Headwear .
    ?Headwear a ?HeadwearClass .
    ?HeadwearClass rdfs:subClassOf* wt:Headwear .
"""
JewelryQuery = """
    ?Person wt:isWearing ?Jewelry .
    ?Jewelry a ?JewelryClass .
    ?JewelryClass rdfs:subClassOf* wt:Jewelry .
"""
EarringsQuery = """
    ?Person wt:isWearing ?Earrings .
    ?Earrings a ?EarringsClass .
    ?EarringsClass rdfs:subClassOf* wt:Earrings .
"""
NecklaceQuery = """
    ?Person wt:isWearing ?Necklace .
    ?Necklace a ?NecklaceClass .
    ?NecklaceClass rdfs:subClassOf* wt:Necklace .
"""
MakeupQuery = """
    ?Person wt:isWearing ?Makeup .
    ?Makeup a ?MakeupClass .
    ?MakeupClass rdfs:subClassOf* wt:Makeup .
"""
LipstickQuery = """
    ?Person wt:isWearing ?Lipstick .
    ?Lipstick a ?LipstickClass .
    ?LipstickClass rdfs:subClassOf* wt:Lipstick .
"""
NeckTieQuery = """
    ?Person wt:isWearing ?NeckTie .
    ?NeckTie a ?NeckTieClass .
    ?NeckTieClass rdfs:subClassOf* wt:NeckTie .
"""

PosedImageQuery = """
    ?Image a img:PosedImage.
"""
BlackAndWhiteImageQuery = """
    ?Image a img:BlackAndWhiteImage.
"""
CandidImageQuery = """
    ?Image a img:CandidImage.
"""
ColorImageQuery = """
    ?Image a img:ColorImage.
"""

DepictedBackgroundQuery = """
    ?Image lio:hasDepictedBackground ?DepictedBackground .
    ?DepictedBackground a ?DepictedBackgroundClass .
    ?DepictedBackgroundClass rdfs:subClassOf* img:DepictedBackground .
"""
IndoorsQuery = """
    ?Image lio:hasDepictedBackground ?DepictedBackground .
    ?DepictedBackground a img:Indoors .
"""
OutdoorsQuery = """
    ?Image lio:hasDepictedBackground ?DepictedBackground .
    ?DepictedBackground a img:Outdoors .
"""


ImageFidelityQuery = """
    ?Image img:fidelityDescribedBy ?ImageFidelity .
    ?ImageFidelity a ?ImageFidelityClass .
    ?ImageFidelityClass rdfs:subClassOf* img:ImageFidelity .
"""
BlurryImageFidelityQuery = """
    ?Image img:fidelityDescribedBy ?ImageFidelity .
    ?ImageFidelity a img:BlurryImageFidelity .
"""
SharpImageFidelityQuery = """
    ?Image img:fidelityDescribedBy ?ImageFidelity .
    ?ImageFidelity a img:SharpImageFidelity .
"""



LightingVariationQuery = """
    ?Image img:lightingDescribedBy ?LightingVariation .
    ?LightingVariation a ?LightingVariationClass .
    ?LightingVariationClass rdfs:subClassOf* img:LightingVariation .
"""
BalancedLightingVariationQuery = """
    ?Image img:lightingDescribedBy ?LightingVariation .
    ?LightingVariation a img:BalancedLightingVariation .
"""

HarshLightingVariationQuery = """
    ?Image img:lightingDescribedBy ?LightingVariation .
    ?LightingVariation a ?LightingVariationClass .
    ?LightingVariationClass rdfs:subClassOf* img:HarshLightingVariation .
"""
FlashLightingVariationQuery = """
    ?Image img:lightingDescribedBy ?LightingVariation .
    ?LightingVariation a img:FlashLightingVariation .
"""
SoftLightingVariationQuery = """
    ?Image img:lightingDescribedBy ?LightingVariation .
    ?LightingVariation a img:SoftLightingVariation .
"""




obo = "http://purl.obolibrary.org/obo/"
pfd = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/"
ho = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/"
wt = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/WearableThingsOntology/"
img = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/"

querymapper = {
    lio + "Image" : "",
    frma + "MugShotPhoto": mugshotQuery,
    frma + "Occlusion": occlusionQuery,
    frma + "CervicalOcclusion" : cervicalOcclusionQuery,
    frma + "FaceOcclusion" : FaceOcclusionQuery,
    frma + "LowerFaceOcclusion" : LowerFaceOcclusionQuery,
    frma + "UpperFaceOcclusion" : UpperFaceOcclusionQuery,
    frma + "BuccalOcclusion" : BuccalOcclusionQuery,
    frma + "OralOcclusion" : OralOcclusionQuery,
    frma + "MentalOcclusion" : MentalOcclusionQuery,
    frma + "ParotidOcclusion" : ParotidOcclusionQuery,
    frma + "ZygomaticOcclusion" : ZygomaticOcclusionQuery,

    frma + "AuricleOcclusion" : AuricleOcclusionQuery,
    frma + "CranialOcclusion" : CranialOcclusionQuery,
    frma + "FrontalOcclusion" : FrontalOcclusionQuery,
    frma + "OcularOcclusion" : OcularOcclusionQuery,
    frma + "NasalOcclusion" : NasalOcclusionQuery,

    lio + "PictorialElement" : "",
    pfd + "Person" : "",

    obo + "UBERON_0001567" : CheekQuery,
    pfd + "HighCheekbones" : HighCheekQuery,
    pfd + "RosyCheeks" : RosyCheekQuery,

    obo + "UBERON_0008199" : ChinQuery,
    pfd + "DoubleChin" : DoubleChinQuery,
    pfd + "RoundJaw" : RoundJawQuery,

    pfd + "Demographic" : DemographicQuery,
    pfd + "AgeRange" : AgeRangeQuery,
    pfd + "Baby" : BabyQuery,
    pfd + "Child" : ChildQuery,
    pfd + "MiddleAged" : MiddleAgedQuery,
    pfd + "Senior" : SeniorQuery,
    pfd + "Youth" : YouthQuery,

    pfd + "Ethnicity" : EthnicityQuery,
    pfd + "Asian" : AsianQuery,
    pfd + "Black" : BlackQuery,
    pfd + "Indian" : IndianQuery,
    pfd + "White" : WhiteQuery,

    pfd + "GenderExpression" : GenderExpressionQuery,
    pfd + "Feminine" : FeminineQuery,
    pfd + "Masculine" : MasculineQuery,

    pfd + "WeightRange" : WeightRangeQuery,
    pfd + "Skinny" : SkinnyQuery,
    pfd + "Chubby" : ChubbyQuery,

    pfd + "FaceShape" : FaceShapeQuery,
    pfd + "OvalFace" : OvalFaceQuery,
    pfd + "RoundFace" : RoundFaceQuery,
    pfd + "SquareFace" : SquareFaceQuery,

    pfd + "FacialExpression" : FacialExpressionQuery,
    pfd + "ArchedEyebrow" : ArchedEyebrowQuery,
    pfd + "Frowning" : FrowningQuery,
    pfd + "NarrowEyes" : NarrowEyesQuery,
    pfd + "Smiling" : SmilingQuery,

    ho + "Hair" : HairQuery,
    ho + "FacialHair" : FacialHairQuery,
    ho + "HeadHair" : HeadHairQuery,

    ho + "Beard" : BeardQuery,
    ho + "FiveOClockShadow" : FiveOClockShadowQuery,
    ho + "Goatee" : GoateeQuery,

    ho + "Eyebrows" : EyebrowsQuery,
    ho + "BushyEyebrows" : BushyEyebrowsQuery,
    ho + "ThinEyebrows" : ThinEyebrowsQuery,

    ho + "Mustache" : MustacheQuery,
    ho + "Sideburn" : SideburnQuery,

    ho + "HairTexture" : HairTextureQuery,
    ho + "CurlyHair" : CurlyHairQuery,
    ho + "StraightHair" : StraightHairQuery,
    ho + "WavyHair" : WavyHairQuery,

    ho + "Haircut" : HaircutQuery,
    ho + "Balding" : BaldingQuery,
    ho + "LongHair" : LongHairQuery,
    ho + "Bald" : BaldQuery,
    ho + "RecedingHairline" : RecedingHairlineQuery,
    ho + "Bangs" : BangsQuery,

    pfd + "SkinTone" : SkinToneQuery,
    pfd + "Flush" : FlushQuery,
    pfd + "Pale" : PaleQuery,

    wt + "WearableObject" : WearableObjectQuery,
    wt + "Headwear" : HeadwearQuery,
    wt + "Eyewear" : EyewearQuery,
    wt + "Eyeglasses" : EyeglassesQuery,
    wt + "Sunglasses" : SunglassesQuery,
    wt + "Hat" : HatQuery,

    wt + "Ornament" : OrnamentQuery,
    wt + "Jewelry" : JewelryQuery,
    wt + "Earrings" : EarringsQuery,
    wt + "Necklace" : NecklaceQuery,
    wt + "Makeup" : MakeupQuery,
    wt + "Lipstick" : LipstickQuery,
    wt + "NeckTie" : NeckTieQuery,

    img + "BlackAndWhiteImage" : BlackAndWhiteImageQuery,
    img + "CandidImage" : CandidImageQuery,
    img + "ColorImage" : ColorImageQuery,
    img + "PosedImage" : PosedImageQuery,

    img + "DepictedBackground" : DepictedBackgroundQuery,
    img + "Indoors" : IndoorsQuery,
    img + "Outdoors" : OutdoorsQuery,

    img + "ImageFidelity" : ImageFidelityQuery,
    img + "BlurryImageFidelity" : BlurryImageFidelityQuery,
    img + "SharpImageFidelity" : SharpImageFidelityQuery,

    img + "LightingVariation" : LightingVariationQuery,
    img + "BalancedLightingVariation" : BalancedLightingVariationQuery,
    img + "HarshLightingVariation" : HarshLightingVariationQuery,
    img + "FlashLightingVariation" : FlashLightingVariationQuery,
    img + "SoftLightingVariation" : SoftLightingVariationQuery,
}
