#include <bts/blockchain/types.hpp>
#include <fc/crypto/elliptic.hpp>
#include <fc/io/json.hpp>
#include <fc/filesystem.hpp>

#include <iostream>

using namespace bts::blockchain;

int main( int argc, char** argv )
{
   if( argc != 2 )
   {
      std::cerr << "usage: pts_public_key_from_private PRIVATE_KEY_JSON\n";
      return 1;
   }

   try
   {
      fc::ecc::private_key key =
         fc::json::from_file( fc::path(argv[1]) )
            .as<fc::ecc::private_key>();

      std::cout
         << std::string( public_key_type(key.get_public_key()) )
         << "\n";

      return 0;
   }
   catch( const std::exception& e )
   {
      std::cerr << "ERROR: unable to read private key\n";
      return 1;
   }
}
