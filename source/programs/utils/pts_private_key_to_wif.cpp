#include <bts/utilities/key_conversion.hpp>
#include <fc/crypto/elliptic.hpp>
#include <fc/io/json.hpp>
#include <fc/filesystem.hpp>
#include <iostream>

int main(int argc, char** argv)
{
    if (argc != 2)
        return 1;

    try
    {
        fc::ecc::private_key key =
            fc::json::from_file(fc::path(argv[1])).as<fc::ecc::private_key>();

        std::cout << bts::utilities::key_to_wif(key) << "\n";
        return 0;
    }
    catch (...)
    {
        std::cerr << "ERROR\n";
        return 1;
    }
}
