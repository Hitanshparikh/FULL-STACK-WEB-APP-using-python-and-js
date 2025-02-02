import {
    Button,
    Flex,
    FormControl,
    FormLabel,
    Input,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Radio,
    RadioGroup,
    Textarea,
    useDisclosure,
} from "@chakra-ui/react";
import { useToast } from "@chakra-ui/react"; // Updated import
import { useState } from "react";
import PropTypes from "prop-types";
import { BiAddToQueue } from "react-icons/bi";
import { BASE_URL } from "../App";

const CreateUserModal = ({ setUsers }) => {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const [isLoading, setIsLoading] = useState(false);
    const [inputs, setInputs] = useState({
        name: "",
        role: "",
        description: "",
        gender: "",
        email: "",
        age: "",
        mobile: "",
        imgUrl: "",
    });
    const toast = useToast(); // Ensure this is correctly imported

    const handleCreateUser = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const res = await fetch(BASE_URL + "/friends", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(inputs),
            });

            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error);
            }

            toast({
                status: "success",
                title: "Yayy! 🎉",
                description: "Friend created successfully.",
                duration: 2000,
                position: "top-center",
            });
            onClose();
            setUsers((prevUsers) => [...prevUsers, data]);

            setInputs({
                name: "",
                role: "",
                description: "",
                gender: "",
                email: "",
                age: "",
                mobile: "",
                imgUrl: "",
            });
        } catch (error) {
            toast({
                status: "error",
                title: "An error occurred.",
                description: error.message,
                duration: 4000,
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <Button onClick={onOpen}>
                <BiAddToQueue size={20} />
            </Button>

            <Modal isOpen={isOpen} onClose={onClose}>
                <ModalOverlay />
                <form onSubmit={handleCreateUser}>
                    <ModalContent>
                        <ModalHeader> My new BFF 😍 </ModalHeader>
                        <ModalCloseButton />

                        <ModalBody pb={6}>
                            <Flex alignItems={"center"} gap={4}>
                                <FormControl>
                                    <FormLabel>Full Name</FormLabel>
                                    <Input
                                        placeholder='John Doe'
                                        value={inputs.name}
                                        onChange={(e) => setInputs({ ...inputs, name: e.target.value })}
                                    />
                                </FormControl>

                                <FormControl>
                                    <FormLabel>Role</FormLabel>
                                    <Input
                                        placeholder='Software Engineer'
                                        value={inputs.role}
                                        onChange={(e) => setInputs({ ...inputs, role: e.target.value })}
                                    />
                                </FormControl>

                                <FormControl>
                                    <FormLabel>Email</FormLabel>
                                    <Input
                                        placeholder='example@example.com'
                                        value={inputs.email}
                                        onChange={(e) => setInputs({ ...inputs, email: e.target.value })}
                                    />
                                </FormControl>
                            </Flex>

                            <FormControl mt={4}>
                                <FormLabel>Description</FormLabel>
                                <Textarea
                                    resize={"none"}
                                    overflowY={"hidden"}
                                    placeholder="He's a software engineer who loves to code and build things."
                                    value={inputs.description}
                                    onChange={(e) => setInputs({ ...inputs, description: e.target.value })}
                                />
                            </FormControl>

                            <FormControl mt={4}>
                                <FormLabel>Age</FormLabel>
                                <Input
                                    placeholder="25"
                                    value={inputs.age}
                                    onChange={(e) => setInputs({ ...inputs, age: e.target.value })}
                                    type="number"
                                />
                            </FormControl>

                            <FormControl mt={4}>
                                <FormLabel>Mobile Number</FormLabel>
                                <Input
                                    placeholder="123-456-7890"
                                    value={inputs.mobile}
                                    onChange={(e) => setInputs({ ...inputs, mobile: e.target.value })}
                                />
                            </FormControl>

                            <FormControl mt={4}>
                                <FormLabel>Image URL (Optional)</FormLabel>
                                <Input
                                    placeholder="http://example.com/image.jpg"
                                    value={inputs.imgUrl}
                                    onChange={(e) => setInputs({ ...inputs, imgUrl: e.target.value })}
                                />
                            </FormControl>

                            <RadioGroup mt={4} value={inputs.gender} onChange={(value) => setInputs({ ...inputs, gender: value })}>
                                <Flex gap={5}>
                                    <Radio value='male'>Male</Radio>
                                    <Radio value='female'>Female</Radio>
                                </Flex>
                            </RadioGroup>
                        </ModalBody>

                        <ModalFooter>
                            <Button colorScheme='blue' mr={3} type='submit' isLoading={isLoading}>
                                Add
                            </Button>
                            <Button onClick={onClose}>Cancel</Button>
                        </ModalFooter>
                    </ModalContent>
                </form>
            </Modal>
        </>
    );
};

CreateUserModal.propTypes = {
    setUsers: PropTypes.func.isRequired,
};

export default CreateUserModal;
